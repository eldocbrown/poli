export function createActionButton(doc, htmlId, dataId, classText, buttonText, clickHandler) {

  const aActionButton = doc.createElement('button')
  aActionButton.id = htmlId
  aActionButton.dataset.dataId = dataId
  aActionButton.className = classText
  aActionButton.innerHTML = buttonText
  aActionButton.addEventListener('click', (event) => clickHandler(event))

  return aActionButton

}
