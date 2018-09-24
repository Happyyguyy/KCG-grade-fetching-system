// listAnswered()
function listUnanswered() {
    if (document.querySelector(".questions").dataset.type !== "unanswered"){
        deleteQuestions();
        document.querySelector(".list-type").textContent = "Unanswered Questions";
        document.querySelector(".questions").dataset.type = "unanswered"

        pending.once("value", function(snapshot){
            console.log(snapshot.val());
            var color = "";
            for (var item in snapshot.val()) {
                createQuestions(item, snapshot.val()[item], color);

            };
        })

    }
}
function listAnswered() {
    if (document.querySelector(".questions").dataset.type !== "answered"){
        deleteQuestions();
        document.querySelector(".list-type").textContent = "Answered Questions";
        document.querySelector(".questions").dataset.type = "answered"

        completed.once("value", function(snapshot){
            var color ="";
            for (var item in snapshot.val()) {
                createQuestions(item, snapshot.val()[item], color);
            }

        })
}}
function listAll() {
    if (document.querySelector(".questions").dataset.type !== "all"){
        deleteQuestions();
        document.querySelector(".list-type").textContent = "All Questions";
        document.querySelector(".questions").dataset.type = "all"

        completed.once("value", function(snapshot){
            var color = "bg-success";
            for (var item in snapshot.val()) {
                createQuestions(item, snapshot.val()[item], color);
            }
        });
        pending.once("value", function(snapshot){
            var color = "bg-warning";
            for (var item in snapshot.val()) {
                createQuestions(item, snapshot.val()[item], color);
            }
        });
    }
}
function createQuestions(key, data, color){

    var questionList = document.querySelector("#questionList");
        var question = document.createElement("div");
        question.setAttribute("class", "card align-center "+color);
        question.setAttribute("style", "cursor:pointer")
        question.setAttribute("data-thread", key);
        question.setAttribute("onclick", "loadQuestion(this.dataset.thread)")
        question.innerHTML = `<h2 class="align-center title">`+data["title"]+`</h2>`;
    questionList.appendChild(question);
}
function deleteQuestions() {
  var cards = document.querySelector("#questionList");
  var cardList = cards.querySelectorAll(".card");
  // console.log("deleteCards()");
  for (i = 0; i < cardList.length; i++) {
    cards.removeChild(cardList[i]);
    }
  }
function loadQuestion(id) {
    // Check both tables for id. Forward data to setter function
    pending.once("value", snapshot => {
        // Checking for Id in pending
        if (snapshot.hasChild(id)) {
            var data = snapshot.child(id).val();
            setContent(id, data);
        }
        else {
            // if not in pending look in completed
            completed.once("value", snapshot => {
                if (snapshot.hasChild(id)) {
                    var data = snapshot.child(id).val();
                    setContent(id, data)
                }
            });
        }
    });
    document.querySelector(".thread").dataset.id = id;
}
function setContent(id, data) {
    // Enables deleteButton if is was disabled
    var deleteButton = document.querySelector("#deleteCard")
    deleteButton.disabled = false;
    deleteButton.classList.remove("bg-secondary", "border-0")
    deleteButton.innerHTML = "Delete Card"

    // Recieves Id and data and sets webpage with content.
    console.log(data);
    var title = data["title"];
    var dateTime = parseInt(data["createdDateTime"]);
    var message = data["message"];
    if (data["answer"]) {
        var answer = data["answer"]["text"];
        var answerDateTime = parseInt(data["answer"]["dateTime"]);
    };
    if (data["comments"]) {
        var comments = data["comments"];
    }
    else {
        var comments = []
    };
    var tagArr = data["tagArr"];
    console.log(title,dateTime,message,answer,answerDateTime,tagArr, comments);

    // Set question heading
    document.querySelector("#questionHeader").textContent = title;

    // Set dateTime
    document.querySelector("#questionDateTime").textContent = new Date(dateTime).toLocaleString();
    document.querySelector("#questionDateTime").dataset.createdDateTime = dateTime;

    // Set subtitle
    document.querySelector("#questionContent").textContent = message;

    // Set Answer
    document.querySelector("#answerBox").textContent = answer;
    document.querySelector("#answerDateTime").textContent = "Last Updated: " + new Date(answerDateTime).toLocaleString();
    document.querySelector("#answerBox").dataset.dateTime = answerDateTime;

    // Clear and reset newTag field
    document.querySelector("#newTag").setAttribute("class", "form-control");
    document.querySelector("#tagList").firstChild.textContent = "";
    document.querySelector("#newTag").value = "";

    // Set Tags
    var tagList = document.querySelector("#tagList");
    deleteTags();
    tagArr.forEach(tag => {
        listTag(tag);
    });

    // Set Comments
    deleteComments();
    document.querySelector("#commentList").innerHTML = `<li class="list-group-item commentCard">No comments</li>`
    if (Object.keys(comments).length !== 0) {
        deleteComments();
        for (var key in comments) {
            console.log(key);
            listComment(comments[key])
        }
    };
}
function listTag(tag) {
    var listElement = document.createElement("li");
    listElement.setAttribute("class", "list-group-item tag");
    listElement.setAttribute("id", tag);
    listElement.innerHTML = `<div class="input-group"><span class="input-group-addon"><button class="btn btn-warning" onclick="removeTag(this.parentElement.parentElement.parentElement.id)">-</button></span><input class="form-control" type="text" value="`+tag+`" onchange="changeTag(this.value)" /></div>`
    tagList.appendChild(listElement);

    listElement.dataset.tag = tag;
}
function newTag() {
    // TODO: include button to remove tag
    var newTag = $("#newTag").val().trim();
    var tagArr = [];
    var tags = document.querySelectorAll(".tag");
    tags.forEach(item => {
        tagArr.push(item.firstChild.lastChild.value);
    });
    console.log(tagArr);
    if (!tagArr.includes(newTag)) {
        if (newTag) {
            var splitTags = new Set(newTag.split(" "));
            document.querySelector("#newTag").setAttribute("class", "form-control");
            document.querySelector("#tagList").firstChild.textContent = "";
            splitTags.forEach(element => {
                listTag(element);
            })
            document.querySelector("#newTag").value = "";
        };
    }
    else if (newTag && tagArr.includes(newTag)) {
        document.querySelector("#newTag").setAttribute("class", "form-control bg-warning");
        document.querySelector("#tagList").firstChild.textContent = "Tag Exists";
    }
}
function deleteTags() {
  var cards = document.querySelector("#tagList");
  var cardList = cards.querySelectorAll(".tag");
  // console.log("deleteCards()");
  for (i = 0; i < cardList.length; i++) {
    cards.removeChild(cardList[i]);
    }
  }
function removeTag(tag) {
    // Remove in databse
    if (document.querySelectorAll("#tagList .tag").length === 1) {
        alert("Cannot remove tag. A card must have at least one tag")
    }
    else {
        document.querySelector("#tagList").dataset.removeTagList += tag + ",";

        // Remove in client
        var tag = "#"+tag;
        var tag = document.querySelector(tag);
        tag.parentElement.removeChild(tag);
    };
}
function changeTag(tag) {
    console.log("changed");
    document.querySelector("#tagList").dataset.removeTagList += tag + ",";
}
function listComment(data) {
    var commentList = document.querySelector("#commentList");
    var commentElement = document.createElement("li");
    commentElement.setAttribute("class", "list-group-item commentCard");

        var label = document.createElement("label");

        var commentText = document.createElement("div");
        commentText.textContent = data["comment"]

        var commentDate = document.createElement("p");
        commentDate.setAttribute("class", "time");
        commentDate.textContent = new Date(parseInt(data["dateTime"])).toLocaleString();

        var deleteButton = document.createElement("input");
        deleteButton.setAttribute("class", "card");
        deleteButton.setAttribute("type", "checkbox")
        deleteButton.hidden = true;
        // deleteButton.value = "Warning";
        deleteButton.setAttribute("data-index", document.querySelectorAll(".commentCard").length)
        deleteButton.addEventListener("click", function (event) {
            if (this.checked) {
                this.parentNode.parentNode.parentNode.classList.add("bg-secondary");
            }
            if (!this.checked) {
                this.parentNode.parentNode.parentNode.classList.remove("bg-secondary")
            }
        })

        var row = document.createElement("label");
        row.setAttribute("class", "row");

        var leftColumn = document.createElement("div");
        leftColumn.setAttribute("class", "col-1 h-100 text-center");

        var rightColumn = document.createElement("div");
        rightColumn.setAttribute("class", "col-11");

        row.appendChild(leftColumn);
        row.appendChild(rightColumn);

        rightColumn.appendChild(commentText);

        leftColumn.appendChild(deleteButton);
        commentText.appendChild(commentDate);

        commentElement.appendChild(row);

    commentList.appendChild(commentElement);

    // Set data-comment, comment-index and data-date-time
    commentElement.setAttribute("data-comment", data["comment"])
    commentElement.setAttribute("data-date-time", data["dateTime"]);
}
function deleteComments() {
    var cards = document.querySelector("#commentList");
    var cardList = cards.querySelectorAll(".commentCard");
    // console.log("deleteCards()");
    if (cardList) {
    for (i = 0; i < cardList.length; i++) {
      cards.removeChild(cardList[i]);
      }
  }
}
function postTime() {
var time = document.querySelector("#questionDateTime").dataset.createdDateTime;
console.log(time);
}
// TODO: Deletecomment
function removeComment(index) {
    // Remove in databse
    if (document.querySelectorAll("#tagList .tag").length === 1) {
        alert("Cannot remove tag. A card must have at least one tag")
    }
    else {
        document.querySelector("#tagList").dataset.removeTagList += tag + ",";

        // Remove in client
        var tag = "#"+tag;
        var tag = document.querySelector(tag);
        tag.parentElement.removeChild(tag);
    };
}
