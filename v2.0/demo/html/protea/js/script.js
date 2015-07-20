var soft = "/protea/";

$(document).on("click", "#ex1", function(){
    loadExample(soft+"examples/PF07974.fa", "#paste_seq");
    return false;
});

$(document).on("click", "#ex2", function(){
    loadExample(soft+"examples/RF00455.fa", "#paste_seq");
    return false;
});

$(document).on("click", "#reset", function(){
    $('#main').load(soft+'form.php', function(){});
    return false;
});

$(document).on("submit", "#formulaire", function(){
    var param = loadParaSoft(soft);
    var formData=new FormData(this);
    loadFormulaire(formData, param[1], param[3]);
    return false;
});

$(document).on("submit", "#form_id", function(){
    var id = document.getElementById("run_id").value;
    loadResultByID(soft, id);
    return false;
});

