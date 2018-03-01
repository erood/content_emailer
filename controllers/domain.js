/**
 * GET /domains
 * List all domains.
 */
const Domain = require('../models/Domain.js');
const async = require('async');

var locals = {};




exports.getDomains = (req, res) => {

  var locals = {};
  var tasks = [
      function(callback){
        Domain.find(function(err, docs) {
          if (err) { return callback(err); }
          if (docs != null){
            locals.domain = docs;
            callback();
          }
          else{
            locals.domain = docs;
            callback();
          }
        });
      },

  ];

  async.parallel(tasks, function(err) {
      if (err) return next(err);
      res.render('domains', locals);
  });
};


//  Domain.find((err, docs) => {
//    res.render('domains', { domains: docs });
//  });
//};
