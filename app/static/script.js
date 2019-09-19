var quill = new Quill('#editor', {
    theme: 'bubble',
    "modules": {
        "toolbar": false,
    },
    readOnly: true,
});
updatedisplay = () => quill.setContents(JSON.parse($("#content").html())["ops"])