const diffLineToWord = require('diff-linetoword');
const getStdin = require('get-stdin');
const JsDiff = require('diff');

getStdin().then(function(line_diff) {
    const patches = JsDiff.parsePatch(line_diff);
    patches.map(diffLineToWord)
        .forEach(function(patch) {
            console.log(patch);
        });
});
