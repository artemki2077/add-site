console.log(blogs_s);
blogs_s = blogs_s.replaceAll('&#39;', '"');

var blogs = JSON.parse(blogs_s);

const blog_edit = new JSONEditor(document.getElementById("blog_edit"), {})

blog_edit.set(blogs)


function save(){
    var s_blog = blog_edit.get()
    $.ajax({
        type: "POST",
        url: '/adminka/blogs',
        data: JSON.stringify(s_blog),
        success: alert,
        contentType: "application/json",
        dataType: 'json'
    });
}