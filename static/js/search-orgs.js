let timer;
let orgSearchInput = document.getElementById("org_search_input");
orgSearchInput.addEventListener("keyup", (e)=>{
    clearTimeout(timer);
    timer = setTimeout(()=>{
        search_orgs(e.target.value);
    }, 500)
})

document.onload = function(){
    search_orgs("");
}

function search_orgs(keyword){
    fetch(`/search_orgs?q=${keyword}`)
        .then((response)=>{
            if(response.ok){
                return response.json()
            }
        })
        .then((data)=>{
            let resultArea = document.getElementById("org_search_result")
            let resultStr = ""
            data.result.forEach((item)=>{
                resultStr += `
                    <a class="dropdown-item fs--1 px-card py-1 hover-primary" href="/organization/switch_to/${item.slug}">
                        <div class="d-flex align-items-center">
                        <span class="fas fa-users mr-2 text-300 fs--2"></span>
                        <div class="font-weight-normal">${item.name}</div>
                        </div>
                    </a>
                `;
            });
            resultArea.innerHTML = resultStr;
        })
}