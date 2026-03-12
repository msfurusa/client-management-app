function openTab(tabName) {
    // Hide all tab contents
    var tabContents = document.getElementsByClassName("tab-content");
    for (var i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = "none";
    }
    
    // Show the selected tab
    document.getElementById(tabName).style.display = "block";
}

function unlinkContact(clientId,contactId){

    fetch(`/unlink/${clientId}/${contactId}`,{
        method:"DELETE"
    })
        .then(res=>res.json())
        .then(()=>{
            location.reload()
        })

}
