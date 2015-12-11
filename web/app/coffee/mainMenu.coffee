class Sputnik.MainMenu extends Backbone.View
  id: 'main-menu'

  initialize: ->
    @template = Sputnik.loadTemplate('mainMenu')

  render: ->
    @$el.html(@template())