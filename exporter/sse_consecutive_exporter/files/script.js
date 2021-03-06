let eventSource;

function start() { // when "Start" button pressed
  
  if (!window.EventSource) {
    // IE or an old browser
    alert("The browser doesn't support EventSource.");
    return;
  }

  eventSource = new EventSource('http://localhost:5678/stream');

  eventSource.onopen = function(e) {
    log("Event: open");
    calculator.start_working();
  };

  eventSource.onerror = function(e) {
    log("Event: error");
    calculator.end_working();
    if (this.readyState == EventSource.CONNECTING) {
      log(`Reconnecting (readyState=${this.readyState})...`);
    } else {
      log("Error has occured.");
    }
  };

  eventSource.addEventListener('bye', function(e) {
    log("Event: bye, data: " + e.data);
    calculator.end_working();
  });

  eventSource.onmessage = function(e) {
    log("Event: message, data: " + e.data);
    new_data(e.data);
  };

}

function stop() { // when "Stop" button pressed
  eventSource.close();
  calculator.end_working();
  log("eventSource.close()");
}

function request_update(service_name) {
  // signal
  calculator.update_incoming(service_name);
  log("request update of service " + service_name);
  
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://localhost:5678/request_update", true);
  xhttp.send(service_name);
  
  log("request sent");
}

class UIStateCalculator {
  constructor(doc) {
    this.document = doc;
  }
  
  get_class_for_state(state) {
    if (state == null) {
      return "bg-grey";
    } else if (state) {
      return "bg-green";
    } else {
      return "bg-red";
    }
  }
  
  get_state_for_classlist(classlist) {
    if (classlist.contains("bg-green")) {
      return true;
    } else if (classlist.contains("bg-red")) {
      return false;
    } else {
      return null;
    }
  }
  
   toInfoRepresentable(info_text) {
    var max_service_info_length = 60;
    
    if (!info_text) {
      return info_text;
    }
    
    if (info_text.length > max_service_info_length) {
      return info_text.slice(0, max_service_info_length-3) + "...";
    }
    return info_text;
  }
  
  toDateRepresentable(otpional_date) {
    var date = null;
    if (otpional_date != null) {
      date = new Date(otpional_date);
    }
    return date.toLocaleString("de-DE");
  }
  
  toLegalName(name) {
    var res = name;
    res = res.replace(/[&<>"'\/]/g,"");
    return res;
  }
  
  replace_innerHTML(element_name, replacement_html) {
    var cont = this.document.getElementById(element_name);
    cont.innerHTML = replacement_html;
  }
  
  calculate_diff(service_obj) {
    var el = this.document.getElementById(service_obj.service_name);
    // the states
    this.is_new = false;
    this.state_changed = false;
    this.info_changed = false;
    this.time_changed = true; // time hopefully always changes.
    
    if (el == null) {
      this.is_new = true;
      // it is clear now.
      return;
    }
    
    var classlist = this.document.getElementById(service_obj.service_name + ".state").children.item(0).classList;
    var old_state_value = this.get_state_for_classlist(classlist)
    if (old_state_value != service_obj.service_state) {
      this.state_changed = true;
    }
    
    var old_info_value = this.document.getElementById(service_obj.service_name + ".info").children.item(0).textContent;
    old_info_value = this.toInfoRepresentable(old_info_value);
    if (old_info_value != service_obj.service_info) {
      this.info_changed = true;
    }
  }

  update_document(service_obj) {
    var state_class = this.get_class_for_state(service_obj.service_state);
    
    var icon = "mif-cog";
    if (service_obj.service_config && service_obj.service_config.exporter_hints && service_obj.service_config.exporter_hints.metro_tile_icon) {
      icon = service_obj.service_config.exporter_hints.metro_tile_icon;
    }
    
    // make a GUI-string this is cut down into a maximum fixed length
    var service_info_representable = this.toInfoRepresentable(service_obj.service_info);
    
    // make a GUI-string, parse format and make viewable format
    var service_time_representable = this.toDateRepresentable(service_obj.service_time);
      
    var state_html = `<div class="icon ${state_class} fg-white flashit"><span class="${icon}"></span></div>`;
    var time_html = `<div class="text-upper text-small flashit">${service_time_representable}</div>`;
    var info_html =  `<div class="text-upper text-small flashit">${service_info_representable}</div>`;
    var badge_html = `<span id="${service_obj.service_name}.badge" style="visibility:hidden" class="badge bg-blue fg-white">!</span>`;
  
    var inner_html = `
            <div class="cell-md-4 mt-4 flashit" id="${service_obj.service_name}" onclick="request_update('${service_obj.service_name}')">
                
                <div class="icon-box border bd-default">
                    <div id="${service_obj.service_name}.state">${state_html}</div>
                    ${badge_html}
                    <div class="content p-4">
                        <div class="text-upper text-bold text-lead">${service_obj.service_name}</div>
                        <div id="${service_obj.service_name}.info">${info_html}</div>
                        <div id="${service_obj.service_name}.time">${time_html}</div>
                    </div>
                </div>
            </div>
    `;
    
    if (this.is_new) {
      var service_group_legalname = this.toLegalName(service_obj.service_config.group);
      // check group already existing:
      var grp = this.document.getElementById(service_group_legalname);
      
      if (grp != null) {
        // group existing, just insert the element at the end
        grp.insertAdjacentHTML("beforeend", inner_html);
      } else {
        // group not existing, add group with heading and the element
        var cont = this.document.getElementById("main_container");
        cont.insertAdjacentHTML("beforeend", `
        <p class="text-secondary fg-white">${service_obj.service_config.group}</p>
        <div class="row mt-2" id="${service_group_legalname}">
            ${inner_html}
        </div>
        `);
      }
      
      return;
    }
    
    if (this.state_changed) {
      this.replace_innerHTML(service_obj.service_name + ".state", state_html);
    }
    if (this.info_changed) {
      this.replace_innerHTML(service_obj.service_name + ".info", info_html);
    }
    if (this.time_changed) {
      this.replace_innerHTML(service_obj.service_name + ".time", time_html);
    }
    // almost always something has changed:
    var el = this.document.getElementById(service_obj.service_name + ".badge");
    el.style.visibility = "hidden";
  }
  
  start_working() {
    var progressor = this.document.getElementById('progressor');
    progressor.classList.add("ani-pulse");
  }

  end_working() {
    var progressor = this.document.getElementById('progressor');
    progressor.classList.remove("ani-pulse");
  }

  update_incoming(service_name) {
    var el = this.document.getElementById(service_name + ".badge");
    el.style.visibility = "visible";
  }
  
  calculate_and_update(service_obj) {
    this.calculate_diff(service_obj);
    this.update_document(service_obj);
  }
  
}

function new_data(msg) {
  var service_obj = JSON.parse(msg);
  
  /*
  What happened:
  1. new service-item appeared: whole item flashing. 
  2. just updated: last-updated-time flashing (optionally deactivable).
  3. info changed: service_info flashing.
  4. state changed: service_state flashing.
  */
  calculator.calculate_and_update(service_obj);
}

function log(msg) {
  console.log(msg);
}

let calculator = new UIStateCalculator(document);
