/**
 * Created by yooyoung-mo on 2016. 2. 9..
 */

var initialize = function (navigator) {
    "use strict";
    $('#id_login').on('click', function () {
        navigator.id.request();
    });
};

window.Superlists = {
    Accounts: {
        initialize : initialize
    }
};

