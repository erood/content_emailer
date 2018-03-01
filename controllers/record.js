/**
 * GET /records
 * List all records.
 */
const Record = require('../models/Record.js');

exports.getRecords = (req, res) => {
  Record.find((err, docs) => {
    res.render('records', { records: docs });
  });
};


exports.postRecords = (req, res, next) => {
    //req.assert('record_weight', 'Please ensure employee type or role is correct').isNumber();
    //req.assert('email', 'Please enter a valid email address.').isEmail();

    const errors = req.validationErrors();

    if (errors) {
      req.flash('errors', errors);
      return res.redirect('/records');
    }
    /* define what needs to be saved*/
    const record = new Record({

      name: req.body.name,
      website: req.body.website,
      description: req.body.description,
      audience: req.body.audience,
      content_type: req.body.content_type,
      open_rate: req.body.open_rate,
      ctr: req.body.ctr,
      pricing: req.body.pricing,
      contact_method: req.body.contact_method,
      email: req.body.email,
    });

    record.save((err) => {
      /* this provides a block if the error is that hte email address is already associated with an employee*/
      if (err) {
        if (err.code === 11000) {
          req.flash('errors', { msg: 'The email address you have entered is already associated with an account.' });
          return res.redirect('/records');
        }
        return next(err);
      }
      console.log("SAVED!");
      req.flash('success', { msg: 'This has been saved!' });
      res.redirect('/records');
});
};
