function newPost() {
  // push a new post to pending

  var newTags = []
  var title = $("#title").val();
  var message = $("#message").val();
  var location = $("#locTag").val();
  var tagsText = $("#tagTag").val();
  var tagArr = tagsText.split(" ");
  var createdDateTime = firebase.database.ServerValue.TIMESTAMP;

// check for empty fields. if empty raise error
  if (![title,message,location,tagsText].every(function(snapshot){return snapshot!== '';})) {
    if (!title) {console.log("no Title")};
    if (!message) {console.log("no message")};
    if (!location) {console.log("no location")};
    if (!tagsText) {console.log("no tagsText")};
    throw "Empty fields";
  };
  var data = {
    'title': title,
    'message': message,
    'locTag': location,
    'createdDateTime': createdDateTime,
    'tagArr': tagArr,
  };
  // if ([title, message, location, tagsText].includes('')) {
  // }
  // else {
    console.log(title, message, location, tagArr, new Date().toLocaleString('en-US'), new Date());

  var key = pending.push(data);
  tagArr.forEach(function(tag){
    firebase.database().ref("tags/"+tag).child(key.key).set("pending");
  })
    // newTags.forEach(function(element) {
    //     var div = document.createElement("div");
    //     div.innerHTML += '<div class="card" id="tags"><span style="margin-left: 15px; font-size:30px;cursor:pointer" onclick="openTwo(this.id)" id="'+ element + '">' +
    //         '<h2 id="TagCard">&#9776; ' +
    //         element +
    //         '</h2></span></div>';
    //     $("#panelOne").append(div);
    //
    // });
    };

function completeCard() {
    // TODO: Get Title
    var key = document.querySelector(".thread").dataset.id;
    var title = document.querySelector('#questionHeader').textContent;

    // TODO: Get createdDateTime
    var createdDateTime = document.querySelector("#questionDateTime").dataset.createdDateTime;

    // TODO: Get message
    var message = document.querySelector("#questionContent").textContent;

    // TODO: Get tagArr
    var tagArr = [];
    var tagArrHTML = document.querySelectorAll(".tag");
    tagArrHTML.forEach(item => {
        var tag = item.firstChild.lastChild.value;
        if (!tagArr.includes(tag)) {
            tagArr.push(tag);
        };
    });
    // TODO: Get answer: text and dateTime
    var answer = {};
    var answerDateTime = document.querySelector("#answerBox").dataset.dateTime;
    answer.text = document.querySelector("#answerBox").value;
    if (!isNaN(answerDateTime)) {
        answer["dateTime"] = answerDateTime;
    }
    else {
        answer["dateTime"] = firebase.database.ServerValue.TIMESTAMP;
    }
    // TODO: Get all comments: comment and dateTime and UID
    comments = [];
    var commentCards = document.querySelectorAll(".commentCard");
    if (commentCards[0].innerText !== "No comments") {
        commentCards.forEach(element => {
            var comData = {};
            comData.comment = element.dataset.comment;
            comData.dateTime = element.dataset.dateTime;
            comments.push(comData);
        })
    }
    // Remove selected comments
    var removeIndexes = [];
    var checkboxList = document.querySelectorAll(".commentCard .row div.text-center input");
    console.log(checkboxList);
    checkboxList.forEach(function(element) {
        var index = element.dataset.index;
        comments.splice(index, 1);
    });
    console.log(comments);
    // Place data in object
    var data = {
        "title": title,
        "createdDateTime": createdDateTime,
        "message": message,
        "tagArr": tagArr,
        "answer": answer,
        "comments": comments
    }

    // If answer entered, complete card
    if (answer.text) {
    // Move card from pending to completed
        completed.child(key).set(data);
        pending.child(key).remove();

        // Remove tags from database[tags]
        var removeListStr = document.querySelector("#tagList").dataset.removeTagList;
        var removeArr = removeListStr.split(",");
        if (removeListStr) {
            removeArr.forEach(element => {
                if (element) {tags.child(element).child(key).remove();};
            });
        };

        // Set card to completed on all tags including new ones
        tagArr.forEach(element => {
            var obj = {}
            obj[key] = "completed";
            tags.child(element).update(obj);
            })

        // Button Update to green
        var button = document.querySelector("#submit");
        button.setAttribute("class", "btn btn-success");
        button.textContent = "Successfully Updated. Card Completed";
        setTimeout(function() {
            button.setAttribute("class", "btn btn-primary");
            button.textContent = "Answer and/or Update"
        }, 1500)
    }
    else if (!answer.text) {
    // Move card from completed to pending
        pending.child(key).set(data);
        completed.child(key).remove();

        // Remove tags from database[tags]
        var removeListStr = document.querySelector("#tagList").dataset.removeTagList;
        var removeArr = removeListStr.split(",");
        if (removeListStr) {
            removeArr.forEach(element => {
                if (element) {tags.child(element).child(key).remove();};
            });
        };

        // Set card to completed on all tags including new ones
        tagArr.forEach(element => {
            var obj = {}
            obj[key] = "pending";
            tags.child(element).update(obj);
            })

        // Button Update to green
        var button = document.querySelector("#submit");
        button.setAttribute("class", "btn btn-secondary");
        button.textContent = "Updated. Pending Answer";
        setTimeout(function() {
            button.setAttribute("class", "btn btn-primary");
            button.textContent = "Answer and/or Update"
        }, 1500)
    }
    // Reload page with updates
    loadQuestion(key);
}
function deleteCardInDatabase() {
    var id = document.querySelector(".thread").dataset.id;
    // Check both tables for id. Forward data to setter function
    pending.once("value", snapshot => {
        // Checking for Id in pending
        if (snapshot.hasChild(id)) {
            pending.child(id).once("value", snapshot => {
                var tagArr = snapshot.val()["tagArr"];
                tagArr.forEach(element => {
                    tags.child(element).child(id).remove();
                })
                pending.child(id).remove();
            })

        }
        else {
            // if not in pending look in completed
            completed.once("value", snapshot => {
                    completed.child(id).once("value", snapshot => {
                        var tagArr = snapshot.val()["tagArr"];
                        tagArr.forEach(element => {
                            tags.child(element).child(id).remove();
                        })
                        completed.child(id).remove();
                    })
            });
        }
    });
    document.querySelector("#deleteCard").disabled = false;
    // document.querySelector(".thread").dataset.id;

}
