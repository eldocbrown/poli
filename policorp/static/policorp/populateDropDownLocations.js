export function populateDropDownLocations(url, dropDown, clickHandler) {
  fetch(url)
  .then(response => response.json())
  .then(data => {
      data.forEach( function(location) {
        const option = document.createElement('a');
        option.classList.add('dropdown-item');
        option.id = 'locationOption';
        option.dataset.locationid = location.id;
        option.innerHTML = location.name;
        option.addEventListener('click', (event) => clickHandler(event));

        dropDown.append(option);
      });
  })
}
