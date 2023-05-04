/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// Select the database to use.
use('DoAnDaNganhDB');

// Insert a few documents into the sales collection.
db.getCollection('Member').insertMany([
  { 'item': '16122002', 'name': 'Nguyen Trong Tin','status': 0, 'date': new Date() },
  { 'item': '22121212', 'name': 'ABC','status': 0, 'date': new Date() },
  { 'item': '11212332', 'name': 'BCDS','status': 0, 'date': new Date() },
  { 'item': '16212121', 'name': 'LOLkdiwjx','status': 0, 'date': new Date() },
  { 'item': '21212211', 'name': 'UQsdj','status': 0, 'date': new Date() },
]);

