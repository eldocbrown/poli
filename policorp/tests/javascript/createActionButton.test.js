/**
 * @jest-environment jsdom
 */

import { createActionButton } from '../../static/policorp/createActionButton.js'

describe('createActionButton', () => {

  it('renders an html button with an event handler', () => {

    document.body.innerHTML ='<div id="container"></div>'

    const mockHandler = jest.fn()

    const element = createActionButton(document, 'availabilityCancelButton', '1', 'btn btn-danger', 'Cancel', mockHandler)

    expect(element).toBeDefined()

    document.querySelector('#container').append(element)

    expect(document.querySelector('#container').innerHTML).toEqual('<button id="availabilityCancelButton" data-data-id="1" class="btn btn-danger">Cancel</button>')

    // Click the button
    element.dispatchEvent(new Event('click'))

    // Expect that the handler was assigned and called when button is clicked
    expect(mockHandler).toBeCalled()
  })
})
