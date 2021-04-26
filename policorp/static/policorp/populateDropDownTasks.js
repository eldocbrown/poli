import { toFormattedDuration } from './dateTimeUtils.js'

export function populateDropDownTasks(url, dropDown, clickHandler) {
  fetch(url)
  .then(response => response.json())
  .then(data => {
      data.forEach( function(task) {
        const option = document.createElement('a');
        option.classList.add('dropdown-item');
        option.id = 'taskOption';
        option.dataset.taskid = task.id;
        option.dataset.duration = task.duration;
        option.innerHTML = `${task.name} (${toFormattedDuration(task.duration)})`;
        option.addEventListener('click', (event) => clickHandler(event));

        dropDown.append(option);
      });
  })
}
