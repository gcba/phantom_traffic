window.Sputnik = {}

class Sputnik.App extends Backbone.View
  events:
    'keypress input': 'onKeyPress'
    'click #keep-signin': 'toggleKeep'
    'click #login-btn': 'attemptLogin'

  onKeyPress: (e) =>
    code = e.keyCode || e.which
    if code == 13
      @attemptLogin()

  toggleKeep: =>
    @$el.find('#keep-signin').toggleClass('active')

  attemptLogin: =>
    data = {
      username: @$el.find('#username').val()
      password: @$el.find('#password').val()
      keep_signed: @$el.find('#keep-signin').hasClass('active')
    }
    console.log(data)
