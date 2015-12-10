class Sputnik.MainMenu extends Backbone.View
  id: 'main-menu'
  className: 'animated fadeIn'

  initialize: ->
    @template = Sputnik.loadTemplate('mainMenu')

  render: ->
    @$el.html(@template())