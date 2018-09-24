var panelOne = document.querySelector("#panelOne");
var panelTwo = document.querySelector("#panelTwo");
var panelThree = document.querySelector("#panelThree");

panelOne.dataset.state = "extended";
panelTwo.dataset.state = "closed";
panelThree.dataset.state = "closed";
// states are "open","extended","closed"

var open = 25;
var extended = 35;
var closed = 0;

function alignPanels () {

  // var rightEdge = 25;
  // var extendPanel = 10;
  // var retractPanel = -10;
  // var openPanel = 25;
  // var openExtendedPanel = 35;
  // var closePanel = -25;
  // var closeExtendedPanel = -35;

  var panelOneState = panelOne.dataset.state;
  var panelTwoState = panelTwo.dataset.state;
  var panelThreeState = panelThree.dataset.state;
  // states are "open","extended","closed"

  if (panelOneState === "extended" && panelTwoState === "closed" && panelThreeState === "closed") {
    panelTwo.style.marginLeft = extended + "%";
    panelThree.style.marginLeft = extended + "%";
  }
  else if (panelOneState === "open" && panelTwoState === "extended" && panelThreeState === "closed") {
    panelTwo.style.marginLeft = open + "%";
    panelThree.style.marginLeft = open + extended + "%";
  }
  else if (panelOneState === "open" && panelTwoState === "open" && panelThreeState === "extended") {
    panelTwo.style.marginLeft = open + "%";
    panelThree.style.marginLeft = open + open + "%";
  }
  // if (panelOneExtended === "true") {
  //   panelOne.style.width = "35%";
  //   panelTwo.style.marginLeft = "35%";
  //   panelThree.style.marginLeft = "35%";
  // }
  // else if (panelOneExtended === "false"){
  //   panelOne.style.width = "25%";
  //   panelTwo.style.marginLeft = "25%";
  //   panelThree.style.marginLeft = "25%";
  // };
  // if (panelTwoExtended === "true" && panelTwoOpen === "true") {
  //   panelTwo.style.width = "35%";
  //   panelThree.style.marginLeft = "60%";
  // }
  // else if (panelTwoExtended === "false" && panelTwoOpen === "true") {
  //   panelTwo.style.width = "25%";
  //   panelThree.style.marginLeft = "50%";
  // };
  // else if (panelTwoOpen === "false") {
  //   panelTwo.style.width = "0%";
  //   panelThree.style.marginLeft = ""
  // }
  // }
}

function closePanelThree() {
  panelThree.style.width = 0 + "%";
  panelTwo.style.width = extended + "%";

  panelThree.dataset.state = "closed";
  panelTwo.dataset.state = "extended";

  alignPanels();

}

function closePanelTwo() {
  panelThree.style.width = 0 + "%";
  panelTwo.style.width = 0 + "%";
  panelOne.style.width = extended + "%";

  panelOne.dataset.state = "extended";
  panelTwo.dataset.state = "closed";
  panelThree.dataset.state = "closed";

  alignPanels();
}

function openPanelTwo(tag) {
  closePanelThree();
  panelOne.style.width = open + "%";
  panelTwo.style.width = extended + "%";

  panelOne.dataset.state = "open";
  panelTwo.dataset.state = "extended";

  panelTwo.dataset.tag = tag;


  alignPanels()

}

function openPanelThree(thread) {
  panelTwo.style.width = open + "%";
  panelThree.style.width = extended + "%";

  panelTwo.dataset.state = "open";
  panelThree.dataset.state = "extended";

  panelThree.dataset.thread = thread;
  alignPanels();
}
function createCard(object) {
  var cards = document.querySelector("#cards");
  var homeTag = document.querySelector("#panelTwo").dataset.tag;

  cardContent = object.val();

  var id = object.key;
  var title = cardContent["title"];
  var message = cardContent["message"];
  var time = new Date(parseInt(cardContent["createdDateTime"])).toLocaleString();

  var card = document.createElement('div');
  card.setAttribute("class", "card");
  card.setAttribute("id", object.key);
  card.setAttribute("data-thread", id);

  card.innerHTML = `
  <span style="font-size:30px;cursor:pointer" onclick="populateComments(this.parentElement.id)">
      <div class="card-body p-1">
      <h4 class="card-title text-left">`+title+`</h4>
          <h6 class="comment">`+message+`</h6>
          <p class="time">Created: `+time+`</p>
      </div>
      </span>
  `
  cards.appendChild(card);

  tags.child(homeTag).child(id).once("value").then(snapshot => {
      card.setAttribute("data-completed", snapshot.val())
      // console.log(snapshot.val());
  });

}

function populateCards(tag, type){

      var showUnanswered = document.querySelector("#showUnanswered").checked;
      console.log(showUnanswered);
      console.log("rerun");
      var cardListHeading = panelTwo.dataset.tag;

      if (cardListHeading !== tag || showUnanswered || type) {
        document.querySelector("#cardListHeading").textContent = tag;
        closePanelTwo();
        deleteCards();
        firebase.database().ref("tags").child(tag).once("value", function(snapshot){
            console.log(snapshot.val());
         for (var key in snapshot.val()) {
           var value = snapshot.val()[key];
           console.log("..."+value);
           if (value === "completed"){
               console.log("......completed");
             completed.child(key).once("value", createCard);
           }
           else if (showUnanswered && value === "pending") {
               console.log("......pending");
               pending.child(key).once("value", createCard);
           }
          }
        });
        openPanelTwo();
      }
      // skips script and opens already loaded panel
      else if (cardListHeading === tag && panelTwo.dataset.state === "closed") {
        openPanelTwo();
      }
     panelTwo.dataset.tag = tag;


}

function deleteCards() {
  var cards = document.getElementById("cards");
  var cardList = document.querySelector("#cards").querySelectorAll(".card");
  // console.log("deleteCards()");
  for (i = 0; i < cardList.length; i++) {
    cards.removeChild(cardList[i]);
    }
    panelTwo.dataset.tag = "";
  }

function populateTags(snapshot) {
  var tagList = document.querySelector("#tagList");
  var id = snapshot.key;
  var tag = document.createElement('div');
    tag.setAttribute("class", "card");
    tag.setAttribute("id", id);
    tag.innerHTML = `<span class="align-middle" style="font-size:30px;cursor:pointer; text-align:center" onclick="populateCards(this.parentElement.id)"><h1 class="title">&#9776; `+id+'<h1></span>'
    tagList.appendChild(tag);
}

function createComment(commentData)  {

  var comment = commentData["comment"];
  var timeStamp = new Date(parseInt(commentData["dateTime"])).toLocaleString();

  var commentList = document.querySelector("#commentList");
  // var listLength = commentList.children.length;

  var commentCard = document.createElement('div');
  commentCard.setAttribute("class", "card comCard");
  // commentCard.database.row = listLength;
  // commentCard.setAttribute("class", "comCard")

    var commentText = document.createElement('h5');
    commentText.setAttribute("class", "comment");
    commentText.textContent = comment;
    commentCard.appendChild(commentText);

    var commentTime = document.createElement('p');
    commentTime.setAttribute("class", "time");
    commentTime.textContent = "Time: " + timeStamp;
    commentCard.appendChild(commentTime);

  commentList.appendChild(commentCard);
}
// var text = "This question has not been answered yet.";
// var dateTime = "";

function populateComments(key, direct= false) {
  var thread = panelThree.dataset.thread;
  var showUnanswered = document.querySelector("#showUnanswered").checked;
  var answeredState = document.getElementById(key).dataset.completed;

  if (thread !== key) {
    deleteComments();
    openPanelThree();
    // Set Answer; Set it to default if it doesn't exist
    completed.child(key).child("answer").once("value", snapshot => {
        console.log(snapshot.val())
        if (snapshot.val() !== null) {
            var text = snapshot.val()["text"];
            var dateTime = "Answered: " + new Date(snapshot.val()["dateTime"]).toLocaleString();
        }
        else {
            var text = "This question has not been answered yet.";
            var dateTime = "";
        }
        document.querySelector("#answerDateTime").textContent = dateTime;
        document.querySelector("#answerText").textContent = text;

    })
    // Create List of comments; if none post default
    completed.child(key).once("value").then(function (snapshot) {
        console.log("in");
        if (snapshot.hasChild("comments")) {
            console.log(snapshot.val()["comments"]);
              for (var comment in snapshot.val()["comments"]) {
                  console.log(comment);
                  createComment(snapshot.val()["comments"][comment])
              }
        }
    }).catch(error => console.log(error))
    // completed.child(key).child("comments").once("value", function(snapshot){
    //     console.log(snapshot.val());
    //     if (snapshot.val()) {
    //       for (var key in snapshot.val()) {
    //           createComment(snapshot.val()[key])
    //       }
    //     }
    //     else {
    //         pending.child(key).child("comments").once("value", function(snapshot) {
    //             if (snapshot.val()) {
    //                 for (var key in snapshot.val()) {
    //                     createComment(snapshot.val()[key])
    //                 }
    //             }
    //             else {
    //                 var commentList = document.querySelector("#commentList");
    //                     var commentCard = document.createElement('div');
    //                     commentCard.setAttribute("class", "card comCard");
    //                     commentCard.textContent = "No Comments";
    //                 commentList.appendChild(commentCard);
        //         }
        //     })
        // }
  // };
  // Set data regarding what comments are being shown.
  panelThree.dataset.thread = key;
  panelThree.dataset.completed = answeredState;

  }
  if (thread === key && panelThree.dataset.state === "closed") {
    openPanelThree();
  }
}

function deleteComments() {
  var commentBox = document.querySelector("#commentBoxDiv");
  if (commentBox) {
      commentBox.parentNode.removeChild(commentBox);
  }
  var commentList = document.querySelectorAll(".comCard");

  commentList.forEach(function(element){
    element.parentNode.removeChild(element);
  });
}
// TODO: Add function to search tags
// TODO: Add function to search cards

// TODO: Make commenting work
function drawCommentBox() {
    var commentBoxDiv = document.querySelector("#commentBoxDiv")

    if (commentBoxDiv) {return}
    else {
        var commentBox = document.createElement("div");
        commentBox.setAttribute("id", "commentBoxDiv");
        commentBox.innerHTML =`
        <div class="card">
            <div class="card-header text-left font-weight-bold">
                Add Reply!
            </div>
            <textarea class="form-control border-0" id="commentBox" rows="4" style="margin-top:10px;"></textarea>
            <button type="submit" class="btn btn-primary" id="postComment" onclick="submitComment(this.previousElementSibling.value.trim())">Post Comment</button>
        `
        document.querySelector("#panelThree").appendChild(commentBox);
        document.querySelector("#commentBox").focus();
    }
}
function submitComment(text) {
    if (!text) {return};
    var uid = firebase.auth().currentUser.uid;
    var thread = document.querySelector("#panelThree").dataset.thread;
    var location = document.querySelector("#panelThree").dataset.completed;
    console.log(thread, location);

    if (location === "completed") {
        completed.child(thread).once("value").then(snapshot => {
            var newComment = {};
            newComment["comment"] = text;
            newComment["dateTime"] = firebase.database.ServerValue.TIMESTAMP;
            newComment["user"] = uid;
            completed.child(thread).child("comments").push(newComment);
            console.log(newComment);

            // Update comment list with new comment
            // Modify timestamp to be valid in client
            newComment["dateTime"] = Math.floor(Date.now());
            createComment(newComment);


        })
    }
    else if (location === "pending") {
        pending.child(thread).once("value").then(snapshot => {
            if (!snapshot.hasChild("comments")) {
            var newComment = {};
            newComment["comment"] = text;
            newComment["dateTime"] = firebase.database.ServerValue.TIMESTAMP
            newComment["user"] = uid;
            pending.child(thread).child("comments").push(newComment).catch(function (error) {
                alert("Stop spamming Comments. Wait a bit");
            });

            // Update comment list with new comment
            // Modify timestamp to be valid in client
            newComment["dateTime"] = Math.floor(Date.now()/1000);
            createComment(newComment);

            }
        })
    }
    document.querySelector("#commentBox").value = "";
}
function search(query, type) {
    console.log(query,type);
    if (type === "tags") {
        var list = document.querySelectorAll("#tagList .card");
        list.forEach(function(element) {
            if (element.id.search(query) === -1) {
                element.hidden = true;
            }
            else {
                element.hidden = false;
            }
        })
    }
    else if (type === "cards") {
        var list = document.querySelectorAll("#cards div");

        list.forEach(function(element) {
            var comment = element.querySelector(".comment");
            var title = element.querySelector(".card-title");

            if (comment.textContent.search(query) === -1 && title.textContent.search(query) === -1) {
                element.hidden = true;
            }
            else {
                element.hidden = false;
            }
        })

    }
}
