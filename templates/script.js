function generateContent() {
  var interests = document.getElementById("interests").value;
  var location = document.getElementById("location").value;
  var friends = document.getElementById("friends").value;
  var age = document.getElementById("age").value;

  fetch('/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ age, location, friends, interests }),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Data received:', data);
    document.getElementById("resultContainer").innerHTML = '<h2>Generated Content:</h2><p>' + data.generated_content + '</p>';
    document.getElementById("resultContainer").setAttribute("data-generated-content", data.generated_content);
    document.getElementById("refineButton").style.display = "block";
  })
  .catch(error => console.error('Error:', error));
}

function refineStory() {
  var generatedContent = document.getElementById("resultContainer").getAttribute("data-generated-content");

  fetch('/refine', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ generated_content: generatedContent }),
  })
  .then(response => response.json())
  .then(data => {
    console.log('New question received:', data.new_question);
    document.getElementById("resultContainer").innerHTML += '<h2>New Question:</h2><p>' + data.new_question + '</p>';
    document.getElementById("resultContainer").innerHTML += '<label for="userResponse">Your response:</label><br><textarea id="userResponse" rows="4" cols="50"></textarea><br>';
    document.getElementById("resultContainer").innerHTML += '<button type="button" onclick="submitResponse()">Submit Response</button>';
  })
  .catch(error => console.error('Error:', error));
}

function submitResponse() {
  var generatedContent = document.getElementById("resultContainer").getAttribute("data-generated-content");
  var userResponse = document.getElementById("userResponse").value;

  fetch('/refined', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ generated_content: generatedContent, new_question_input: userResponse }),
  })
  .then(response => response.json())
  .then(data => {
    console.log('New question received:', data.new_question_output);
    document.getElementById("resultContainer").innerHTML += '<h2>New Question Output:</h2><p>' + data.new_question_output + '</p>';
  })
  .catch(error => console.error('Error:', error));
}
