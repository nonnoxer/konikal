var quill = new Quill('#editor-container', {
    modules: {
        toolbar: [
            [{ 'header': [1, 2, 3, false, 5, 6,] }, { 'font': [] }, { 'size': ['small', false, 'large', 'huge'] }],
            //[{ 'font': [] }, { 'size': ['10px', '20px', '80px'] }],
            ['bold', 'italic', 'underline', 'strike', { 'color': [] }, { 'background': [] }],
            [{ 'script': 'super' }, { 'script': 'sub' }, 'blockquote', 'code-block'],
            ['link', 'image'],
            [{ 'align': [] }],
            [{ 'list': 'ordered' }, { 'list': 'bullet' }, { 'indent': '-1' }, { 'indent': '+1' }]
        ]
    },
    placeholder: 'Start writing...',
    theme: 'snow'
});
updatecontent = () => $("#content").html(JSON.stringify(quill.getContents()));
updateeditor = () => quill.setContents(JSON.parse($("#content").html())["ops"])

updateelevationvalue = () => $("#elevationvalue").text($("#elevationrange").val())