/**
 * GET /
 * Home page.
 */
/*exports.index = (req, res) => {
  res.render('home', {
    title: 'Home'
  });
};*/


/**
 * GET /
 * List all goals.
 */
const async = require('async');
const Goal = require('../models/Goal.js');
const Weight = require('../models/Weight.js');

exports.getGoals = (req, res, next) => {

  var locals = {};
  var tasks = [
      function(callback){
        Goal.find({ 'email': req.user.email }, function (err, docs) {
          if (err) { return callback(err); }
          if (docs != null){
            locals.goal = docs;
            callback();
          }
          else{
            locals.goal = docs;
            callback();
          }
        });
      },

      function(callback){
        //used to sort weight by the log date (needed because a user can back date a weight entry making chart/log out of order)
        Weight.find({ 'email': req.user.email }, function (err, docs1) {
          if (err) { return next(err); }
          if (docs1 != null){
            locals.weight = docs1;
            callback();
          }
          else{
            locals.weight = docs1;
            callback();
          }

        }).sort({"date":-1});
      },

  ];

  async.parallel(tasks, function(err) {
      if (err) return next(err);
      res.render('home', locals);
  });
};


/**
 * POST /
 * Update profile information.
 */
 exports.postGoals = (req, res, next) => {
     //req.assert('goal_weight', 'Please ensure employee type or role is correct').isNumber();
     //req.assert('email', 'Please enter a valid email address.').isEmail();

     const errors = req.validationErrors();

     if (errors) {
       req.flash('errors', errors);
       return res.redirect('/');
     }
     /* define what needs to be saved*/
     const goal = new Goal({
       name: req.user.name,
       email: req.user.email,
       goal_start: req.body.goal_start,
       enter_goals: req.body.enter_goals,
       goal_weight: req.body.goal_weight,
       start_weight: req.body.start_weight,
       goal_date: req.body.goal_date,
       weight_units: req.body.weight_units,
     });

     goal.save((err) => {
       /* this provides a block if the error is that hte email address is already associated with an employee*/
       if (err) {
         if (err.code === 11000) {
           req.flash('errors', { msg: 'The email address you have entered is already associated with an account.' });
           return res.redirect('/');
         }
         return next(err);
       }
       console.log("SAVED!");
       req.flash('success', { msg: 'This has been saved!' });
       res.redirect('/');
 });
 };



 /**
  * POST /
  * Update profile information.
  */
  exports.postWeights = (req, res, next) => {
      //req.assert('goal_weight', 'Please ensure employee type or role is correct').isNumber();
      //req.assert('email', 'Please enter a valid email address.').isEmail();

      const errors = req.validationErrors();

      if (errors) {
        req.flash('errors', errors);
        return res.redirect('/');
      }
      /* define what needs to be saved*/
      const weight = new Weight({
        name: req.user.name,
        email: req.user.email,
        weight: req.body.enter_weight_actual,
        date: req.body.entry_date,
      });


      weight.save((err) => {
        /* this provides a block if the error is that hte email address is already associated with an employee*/
        if (err) {
          if (err.code === 11000) {
            req.flash('errors', { msg: 'The email address you have entered is already associated with an account.' });
            return res.redirect('/');
          }
          return next(err);
        }
        console.log("SAVED!");
        req.flash('success', { msg: 'This has been saved!' });
        res.redirect('/');
  });
  };


//needed for 302 redirect
exports.index = (req, res) => {
  //bringing goals/data in on home page load (copy/pasted getGoals logic in here, that's it)
  //if (req.user) {
  if((req.user)==undefined){
    res.render('home', {
    title: 'Home'
    });
  }
  else
    var locals = {};
    var tasks = [
        function(callback){
            Goal.find({ 'email': req.user.email }, function (err, docs) {
              if (err) { return next(err); }
              if (docs != null){
                locals.goal = docs;
                callback();
              }
              else{
                locals.goal = docs;
                callback();
              }
            });
          },

        function(callback){
          //used to sort weight by the log date (needed because a user can back date a weight entry making chart/log out of order)
          Weight.find({ 'email': req.user.email }, function (err, docs1) {
            console.log(req.user)
            if (err) { return next(err); }
            if (docs1 != null){
              locals.weight = docs1;
              callback();
            }
            else{
              locals.weight = docs1;
              callback();
            }

          }).sort({"date":-1});
        },

    ];
  if((req.user)==undefined){
  }
  else
    async.parallel(tasks, function(err) {
        if (err) return next(err);
        res.render('home', locals);
    });
};
//console.log('user is here')
//}
//exports.index = (req, res) => {
//  res.render('home', {
//    title: 'Home'
//  });
//};

/**
 * POST /signup
 * Create a new local account.
 */
exports.postSignup = (req, res, next) => {
  req.assert('email', 'Email is not valid').isEmail();
  req.assert('password', 'Password must be at least 4 characters long').len(4);
  req.assert('confirmPassword', 'Passwords do not match').equals(req.body.password);
  req.sanitize('email').normalizeEmail({ remove_dots: false });

  const errors = req.validationErrors();

  if (errors) {
    req.flash('errors', errors);
    return res.redirect('/signup');
  }

  const user = new User({
    email: req.body.email,
    password: req.body.password
  });

  User.findOne({ email: req.body.email }, (err, existingUser) => {
    if (err) { return next(err); }
    if (existingUser) {
      req.flash('errors', { msg: 'Account with that email address already exists.' });
      return res.redirect('/signup');
    }
    user.save((err) => {
      if (err) { return next(err); }
      req.logIn(user, (err) => {
        if (err) {
          return next(err);
        }
        res.redirect('/');
      });
    });
  });
};
