window.Sputnik = {
  loadTemplate: (templatePath) ->
    template = undefined
    $.ajax(
      method: 'GET'
      url: "/static/jst/#{templatePath}.jst"
      async: false
      success: (response) ->
        template = _.template(response)
    )
    template
}

class Sputnik.App extends Backbone.View

  initialize: ->
    @login = new Sputnik.Login()

  renderLogin: ->
    @login.render()
    @$el.append(@login.el)