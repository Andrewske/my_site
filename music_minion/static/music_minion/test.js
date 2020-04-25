class dropdown {
    constructor(items) {
        this.inputField = document.querySelector('.chosen-value');
        this.dropdown = $('#playlist-dropdown')
        this.items = items
        this.dropdownArray = [];
    }

    build() {
        this.items.forEach((item) => {
            dropdown.append('<li value="' + item.id + '">' + item.name + '</li>');
        })
        this.dropdownArray = [... document.querySelectorAll('li')];
    }



const inputField = document.querySelector('.chosen-value');
const dropdown = $('#playlist-dropdown')
const dropdownArray = [... document.querySelectorAll('li')];
console.log(typeof dropdownArray)
dropdown.classList.add('open');
inputField.focus(); // Demo purposes only
let valueArray = [];
dropdownArray.forEach(item => {
  valueArray.push(item.textContent);
});

const closeDropdown = () => {
  dropdown.classList.remove('open');
}

inputField.addEventListener('input', () => {
  dropdown.classList.add('open');
  let inputValue = inputField.value.toLowerCase();
  let valueSubstring;
  if (inputValue.length > 0) {
    for (let j = 0; j < valueArray.length; j++) {
      if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
        dropdownArray[j].classList.add('closed');
      } else {
        dropdownArray[j].classList.remove('closed');
      }
    }
  } else {
    for (let i = 0; i < dropdownArray.length; i++) {
      dropdownArray[i].classList.remove('closed');
    }
  }
});

dropdownArray.forEach(item => {
  item.addEventListener('click', (evt) => {
    inputField.value = item.textContent;
    dropdownArray.forEach(dropdown => {
      dropdown.classList.add('closed');
    });
  });
})

inputField.addEventListener('focus', () => {
   inputField.placeholder = 'Type to filter';
   dropdown.classList.add('open');
   dropdownArray.forEach(dropdown => {
     dropdown.classList.remove('closed');
   });
});

inputField.addEventListener('blur', () => {
   inputField.placeholder = 'Select state';
  dropdown.classList.remove('open');
});

document.addEventListener('click', (evt) => {
  const isDropdown = dropdown.contains(evt.target);
  const isInput = inputField.contains(evt.target);
  if (!isDropdown && !isInput) {
    dropdown.classList.remove('open');
  }
});


buildDropdown(
    data['items'],
    $('#playlist-dropdown'),
    'Select a playlist',
);

function buildDropdown(result, dropdown, emptyMessage) {
$('#playlist-dropdown').html();
dropdown.append('<option value="">' + emptyMessage + '</option>');

if(result != '') {
$.each(result, function(k,v) {
dropdown.append('<option value="' + v.id + '">' + v.name + '</option>');
});
}
}