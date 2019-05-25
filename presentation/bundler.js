var asciidoctor = require('asciidoctor.js')();
var asciidoctorRevealjs = require('asciidoctor-reveal.js');
var watch = require('watch');
var express = require('express');
const open = require("open");
asciidoctorRevealjs.register();

const revealjs_dir = '/reveal.js';
const output_dir = 'output';

var options = {
    backend: 'revealjs',
    to_dir: output_dir,
    mkdirs: true,
    attributes: {
        revealjsdir: revealjs_dir
    },
    base_dir: '.',
    to_file: 'index.html'
};
asciidoctor.convertFile('src/source.adoc', options);

watch.createMonitor('./src', monitor => {
    monitor.on('changed', () => {
        asciidoctor.convertFile('src/source.adoc', options);
    })
});

var app = express();
app.use(express.static(output_dir))
app.use(revealjs_dir, express.static('./node_modules/reveal.js'))

app.listen(3000, () => {
    console.log('Presentation running on port localhost:3000');
    open("http://localhost:3000");
});
