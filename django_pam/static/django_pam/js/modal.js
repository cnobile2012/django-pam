/*
 * django-pam
 *
 * by Carl J. Nobile
 *
 * Requires: jQuery, bootstrap, js.cookie, and inheritance
 */

"use strict";


Function.prototype.bind = function(object) {
  var method = this;

  var temp = function () {
    return method.apply(object, arguments);
  };

  return temp;
};


var _BaseModal = Class.extend({

  _csrfSafeMethod: function(method) {
    // These HTTP methods do not require CSRF protection.
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  },

  _setHeader: function() {
    $.ajaxSetup({
      crossDomain: false,
      beforeSend: function(xhr, settings) {
        if (!this._csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        }
      }.bind(this)
    });
  },

  setDefault: function(obj, key, value) {
    if(key in obj) {
      return obj[key];
    } else {
      obj[key] = value;
      return obj[key];
    }
  },

  mimicDjangoErrors: function(data) {
    // Mimic Django error messages.
    var ul = '<ul class="errorlist"></ul>';
    var li = '<li></li>';
    var $tag = null, $errorUl = null, $errorLi = null;
    $('ul.errorlist').remove();

    for(var key in data) {
      $tag = $('select[name=' + key + '], input[name=' + key +
        '], textarea[name=' + key + ']');
      $errorUl = $(ul);

      if($tag.prev().prop('tagName') === 'LABEL') {
        $tag = $tag.prev();
        $errorUl.insertBefore($tag);
      } else if($tag.length === 0 && key === '__all__') {
        $tag = $('div.all-error span');
        $errorUl.appendTo($tag);
      }

      for(let i = 0; i < data[key].length; i++) {
        $errorLi = $(li);
        $errorLi.html(data[key][i]);
        $errorLi.appendTo($errorUl);
      }
    }
  }
});


var ModalAuthenticate = _BaseModal.extend({
  BASE_URL: '/',
  LOGIN_URL: 'accounts/login/',
  LOGOUT_URL: 'accounts/logout/',
  LOGIN: '#dp-login',
  LOGOUT: '#dp-logout',

  init: function() {
    let DP_LOGIN;
    let DP_LOGOUT;
    let DP_BASE_URL;

    if(DP_LOGIN !== (void 0)) {
      this.LOGIN = DP_LOGIN;
    }

    if(DP_LOGOUT !== (void 0)) {
      this.LOGOUT = DP_LOGOUT;
    }

    if(DP_BASE_URL !== (void 0)) {
      this.BASE_URL = DP_BASE_URL;
    }

    var $login = $(this.LOGIN);
    var $logout = $(this.LOGOUT);

    if($login) {
      let DP_LOGIN_URL;

      if(DP_LOGIN_URL !== (void 0)) {
        this.LOGIN_URL = DP_LOGIN_URL;
      }

      $('#modal-login').on('click', function() {
        $login.modal({backdrop: 'static'});
      });
      $('div.modal-footer button[name=login-submit]').on('click',
        {self: this, url: this.BASE_URL + this.LOGIN_URL}, this._loginRequest);
    }

    if($logout) {
      $('#modal-logout').on('click', function() {
        $logout.modal({backdrop: 'static'});
      });
      $('div.modal-footer button[name=logout-submit]').on('click',
          {self: this, url: this.BASE_URL + this.LOGOUT_URL},
          this._logoutRequest);
    }
  },

  _loginRequest: function(event) {
    var self = event.data.self;
    var data = $('div.modal-body form').serializeArray();
    var options = {
      url: event.data.url,
      cache: false,
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8',
      timeout: 20000, // 20 seconds
      success: self._loginCB.bind(self),
      statusCode: {400: self._loginCB.bind(self)},
    };
    self._setHeader();
    $.ajax(options);
  },

  _loginCB: function(data, status) {
    if(status === 'success') {
      document.location.href = data.next;
    } else if(data.responseJSON !== (void 0)) {
      this.mimicDjangoErrors(data.responseJSON);
      $('div.all-error').show();
    } else {
      let $div = $('div.all-error');
      $div.text("Could not contact server.");
      $div.show();
    }
  },

  _logoutRequest: function(event) {
    var self = event.data.self;

  }



});


$(document).ready(function() {
  new ModalAuthenticate();
});
