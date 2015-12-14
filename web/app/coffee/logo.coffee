class Sputnik.Logo extends Backbone.View
  id: 'logo-container'

  initialize: ->
    @template = Sputnik.loadTemplate('logo')

  render: ->
    #TODO detectar load de todos los assets y despues triggear la animacion de intro
    @$el.html(@template())