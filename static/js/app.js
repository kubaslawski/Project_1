document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");


      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;


      // Slides active class change
      this.$slidesContainers.forEach(el => {
        console.log(el.classList);
        el.classList.remove("active");
        console.log(el.classList);


        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
          //console.log(el.dataset.id);
          //console.log(el.classList);
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      //add donation
      var bagQuantity = document.getElementById('bags').value;


      var insArrName = []
      var insArrId = []
      var InstitutionInputs = document.getElementsByName('organization')
      for (var i=0; i<InstitutionInputs.length; i++) {
        if (InstitutionInputs[i].checked) {
          var insId = InstitutionInputs[i].value;
          var insName = InstitutionInputs[i].parentElement.innerText;
          insArrId.push(insId)
          insArrName.push(insName)
        }
      }
      //console.log(insArrName)
      //console.log(insArrId)

      var catArrName = []
      var catArrId = []
      var categoryInputs = document.getElementsByName('categories') // marks all the inputs
      for (var i=0; i<categoryInputs.length; i++) {
        if (categoryInputs[i].checked) {
          var catId = categoryInputs[i].value;
          var catName = categoryInputs[i].parentElement.innerText;
          catArrName.push(catName)
          catArrId.push(catId)
        }
      }
      //console.log(catArrName)
      
      var catArrIdInt = catArrId.map(v => parseInt(v, 10));
      //console.log(catArrIdInt)
      
      var catArrIdString = JSON.stringify(catArrIdInt)
      if (catArrId.length > 0) {
        $.ajax({
          type: "GET",
          url: "/ajax/validate_categories/",
          dataType: "json",
          data: {
            "categories": catArrIdString
          }
        }).done(function(institutionsByName) {
          var len = 0 
          for (var [key, value] of Object.entries(institutionsByName)){
            len = len + 1 
          }
          
          var institutionDiv = document.getElementById("div3")

          if (document.getElementById("div3").className == "active"){
            //console.log("ACTIVE")
            //console.log(len)
          var checkboxLength = document.getElementById("institution-checkbox").childElementCount
            if(checkboxLength>len){
              for(i=len; i=i; i<checkboxLength){
              document.getElementById("institution-checkbox").children[len].remove()
              }

            }
            for (var [name, value] of Object.entries(institutionsByName)){
                  document.getElementById("institution-checkbox").innerHTML +=
                  '<label name="organization_label">' +
                  '<input type="radio" name="organization" value="' + value + '" id="institution-key"/>' +
                  '<span class="checkbox radio"></span>' + 
                  '<span class="description">' + 
                    '<div class="title">'+ name + '</div>' +
                    '<div class="subtitle">' + 
                    '</div>' +
                  '</span>' + 
                '</label>'
          }    
          //if(checkboxLength>len){
          //  for(i=len; i=i; i<checkboxLength){
          //   document.getElementById("institution-checkbox").children[len].remove()
          //  }

          //}

          }
        })
        .fail(function(e) {
          alert( "error" );
          console.log(e)
        })
      }



      


      //warunek 
      
            //aktualizacja widoku
            //na podstawie kategorii renderujemy instytucje - metoda POST (JSON)
            //Wysłanie słownika: id: "name"
            //nowy div - usunąć, dodanie nowych 
            //Usunięcie starej zawartości 
            //DOM 
            //Radio buttons 


      var bagQuantity = document.getElementById('bags').value;
      document.getElementById('summary-quantity').innerHTML = "Oddajesz " + bagQuantity + " worków" + catArrName.join(", ") 
      document.getElementById('summary-institutions').innerHTML = insArrName.join(", ")
      var institutionIdInput = insArrId[0]
      document.getElementById('insId').value = institutionIdInput
      //var type = document.getElementById('id_type').value;

      //document.getElementById("summary-institutions").innerHTML = type


      var street = document.getElementById('street').value;
      var city = document.getElementById('city').value;
      var postcode = document.getElementById('postcode').value;
      var phone = document.getElementById('phone').value;
      var data = document.getElementById('data').value;
      var time = document.getElementById('time').value;
      var comment = document.getElementById('comment').value;

      document.getElementById('street-summary').innerHTML = "Ulica: " + street
      document.getElementById('city-summary').innerHTML = "Miasto: " + city
      document.getElementById('postcode-summary').innerHTML = "Kod pocztowy: " + postcode
      document.getElementById('phone-summary').innerHTML = "Telefon: " + phone
      document.getElementById('data-summary').innerHTML = "Data: " + data
      document.getElementById('time-summary').innerHTML = "Czas: " + time
      document.getElementById('comment-summary').innerHTML = "Komentarze: " + comment
 
      new Request ({
        url: "{% url 'add_donation' %}",
        method: "post",
        data: {
          "quantity": bagQuantity,
          "categories": catArrId.join(", "),
          "institution": catId,
          "address": street,
          "city": city,
          "phone_number": phone,
          "zip_code": postcode,
          "pick_up_data": time,
          "pick_up_time": time,
          "pick_up_comment": comment,
        }
      })
    
    }


    submit(e) {
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  

  function getCookie(c_name)
  {
      if (document.cookie.length > 0)
      {
          c_start = document.cookie.indexOf(c_name + "=");
          if (c_start != -1)
          {
              c_start = c_start + c_name.length + 1;
              c_end = document.cookie.indexOf(";", c_start);
              if (c_end == -1) c_end = document.cookie.length;
              return unescape(document.cookie.substring(c_start,c_end));
          }
      }
      return "";
  }
});
