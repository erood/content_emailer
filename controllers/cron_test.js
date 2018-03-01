//cron job to run python modules
////npm install cron --save
var CronJob = require('cron').CronJob;
const async = require('async');
//npm install python-shell --save
var PythonShell = require('python-shell');
const EventEmitter = require('events');


function runPythonScript() {

  var PythonShell = require('python-shell');

  var pyshell = new PythonShell('py_test.py',{scriptPath:"/Users/erikrood/desktop/creator_ad_app/public/", pythonOptions: ['-u']});

  pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    console.log(message);

  });

  // end the input stream and allow the process to exit
  pyshell.end(function (err) {
    if (err) throw err;
    console.log('finished');
  });

}
// 5 minutes: */5 * * * *
// every minute: * * * * *
// seconds: * * * * * *

//new CronJob('0 6 * * *', function() {
//  console.log('You will see this message everyday at 6am');
//  runPythonScript();
//}, null, true, 'America/Los_Angeles');
