interface SerializedModel {
    pk: number,
    model: string,
    fields: object
}

const roundSelect: HTMLSelectElement = document.querySelector("#round-select")
const participantList: HTMLDivElement = document.querySelector("#participant-list")
const participantPanel: HTMLDivElement = document.querySelector("#participant-panel")
let criteria: Array<SerializedModel> = []

// Automatically select the active round of the event
Array.from(roundSelect.options).forEach((option) => {
    if (option.dataset.status == "active") {
        option.selected = true
        // Manually trigger the change event of select element
        roundSelect.dispatchEvent(new Event("change", { bubbles: true, cancelable: true }))
    }
})

async function handleRoundSelectChange(select: HTMLSelectElement) {
    let roundId = select.options[select.selectedIndex].dataset.id
    displayParticipants(roundId)
    getCriteria(roundId)
    participantPanel.innerHTML = ""
}

async function displayParticipants(roundId: string | number) {
    participantList.innerHTML = ""
    let response = await fetch(`${roundId}/participants`)
    if (response.ok) {
        let participants: Array<SerializedModel> = JSON.parse(await response.json())
        // console.log(participants)
        participants.forEach((participant) => {
            const btn = document.createElement("button")
            btn.classList.add("flex", "items-center", "rounded", "bg-white", "p-1", "gap-4", "focus:bg-gray-300")
            btn.onclick = () => handleParticipantClick(participant, roundId)
            const img = document.createElement("img")
            img.src = `/media/${participant["fields"]["image"]}`
            img.classList.add("object-cover", "rounded", "border", "border-slate-950", "h-10", "w-10")
            const span = document.createElement("span")
            span.textContent = `${participant["fields"]["first_name"]} ${participant["fields"]["last_name"]}`
            span.classList.add("text-slate-950", "font-semibold")
            btn.append(img, span)
            participantList.append(btn)
        })    
    }
}

async function getCriteria(roundId) {
    let response = await fetch(`${roundId}/criteria`)
    if (response.ok) {
        criteria = JSON.parse(await response.json())
    }
}

async function handleParticipantClick(participant: SerializedModel, roundId: string | number) {
    participantPanel.innerHTML = ""
    const div = document.createElement("div")
    div.classList.add("flex", "flex-col", "gap-1")
    const img = document.createElement("img")
    img.src = `/media/${participant["fields"]["image"]}`
    img.classList.add("object-cover", "h-40", "w-40", "border-2", "border-white", "rounded", "self-center")
    const span1 = document.createElement("span")
    span1.innerHTML = `<b>Name:</b> ${participant["fields"]["first_name"]} ${participant["fields"]["last_name"]}`
    div.append(img, span1)
    // Get extra participant data from server
    getExtraParticipantData(div, roundId, participant["pk"])
    participantPanel.append(div)
    checkIfParticipantAlreadyBeenScored(roundId, participant["pk"])
}

async function getExtraParticipantData(div: HTMLDivElement, roundId, participantId) {
    let response = await fetch(`${roundId}/${participantId}/extra-data`)
    if (response.ok) {
        let extraData = await response.json()
        const span2 = document.createElement("span")
        span2.innerHTML = `<b>Candidate number:</b> ${extraData["candidate_number"]}` 
        const span3 = document.createElement("span")
        span3.innerHTML = `<b>Represented entity:</b> ${extraData["represented_entity"]}`
        div.append(span2, span3) 
    }
}

async function checkIfParticipantAlreadyBeenScored(roundId, participantId) {
    let response = await fetch(`${roundId}/${participantId}/check`)
    if (response.ok) {
        showScores(JSON.parse(await response.json()))
    }
    // else showScoringForm()
}

function showScores(scores: Array<SerializedModel>) {
    const div = document.createElement("div")
    div.classList.add("rounded", "text-slate-950")
    const table = document.createElement("table")
    table.classList.add("bg-white")
    const caption = document.createElement("caption")
    caption.textContent = "Scores given"
    caption.classList.add("caption-top", "text-white", "font-semibold")
    table.append(caption)
    criteria.forEach((criterion, i) => {
        const tr = document.createElement("tr")
        const th = document.createElement("th")
        th.textContent = criterion["fields"]["name"]
        th.classList.add("p-1", "border", "border-slate-950")
        const td = document.createElement("td")
        td.textContent = `${scores[i]["fields"]["value"]}/${criterion["fields"]["max_score"]}`
        td.classList.add("p-1", "border", "border-slate-950")
        tr.append(th, td)
        table.append(tr)
    })
    div.append(table)
    participantPanel.append(div)
}

function showScoringForm() {

}