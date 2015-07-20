

/*remplacer example_web_server par le nom de votre dossier*/
var soft = "/NRP2Act/";

$(document).on("submit", "formulaire", function () {
    var form = $(this);
    var decompo = form.attr("decompo");
    var ex = oForm.find("ex1").first().val();
    alert("Form '" + formId + " is being submitted, value of first input is: " + firstValue);
    // Do stuff 
    return false;
})

$(document).on("click", "#ex1", function(){
    loadExample(soft+"example.fasta", "#paste_seq");
    return false;
});

$(document).on("click", "#reset", function(){
    $('#main').load(soft+'form.php #center', function(){});
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




