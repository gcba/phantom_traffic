class Sputnik.Disclaimer extends Backbone.View
  id: 'footer'

  initialize: ->
    @template = Sputnik.loadTemplate('disclaimer')

  render: ->
    @$el.html(@template())