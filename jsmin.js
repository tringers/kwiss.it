const process = require('process');
const UglifyJS = require('uglify-js');
const fs = require('fs');

if (process.argv.length < 4) {
    console.error("Usage: nodejs jsmin.js [input file] [output file]");
} else {
    const data = fs.readFileSync(process.argv[2], 'utf8');
    console.log(data);
    result = UglifyJS.minify(data, {
        toplevel: false,
        mangle: {
            eval: true,
            toplevel: true,
            reserved: [ // TODO: Reservierte Funktionsnamen entfernen und dynamisch in JS die Listener usw. setzen
                'validateEmailaddress',
                'validateUsername',
            ]
        }
    });
    console.log(result.error);
    if (!result.error) {
        fs.writeFileSync(process.argv[3], result.code);
        console.log(result.code);
    }
}