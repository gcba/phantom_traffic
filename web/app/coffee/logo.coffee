class Sputnik.Logo extends Backbone.View
  id: 'logo-container'

  initialize: ->
    @template = Sputnik.loadTemplate('logo')

  render: ->
    @$el.html(@template())