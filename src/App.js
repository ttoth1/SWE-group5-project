import logo from './logo.svg';
import './App.css';
import {useState, useEffect} from 'react';
import {Review} from './Review.js';

function App() {
  const [val, setVal] = useState([])
  function handleDelete(i) {
    setVal([...val.slice(0, i), ...val.slice(i+1)]);
  }

  function handleRatingChange(i, e) {
    const newReviews = val.slice();
    newReviews[i].rating = e.target.value;
    setVal(newReviews);
  }

  function handleCommentChange(i, e) {
    const newReviews = val.slice();
    newReviews[i].comment = e.target.value;
    setVal(newReviews);
  }

  function onClickSave() {
    fetch('/save_reviews', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(val),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      });
  }

  const reviews = val.map(
    (review, i) => <Review 
      movieID={review.movie_id}
      rating={review.rating}
      comment={review.comment}
      onDelete={() => handleDelete(i)}
      onEdit={(e) => handleCommentChange(i, e)}
      onRate={(e) => handleRatingChange(i, e)}
    />);
  
  useEffect(() => {
    fetch('/get_reviews', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then((response) => response.json())
      .then((data) => {
        setVal(data);
      });
  }, []);

  return (
    <div className="App">
      <h1>Your reviews:</h1>
      {reviews}
      <button onClick={onClickSave}>Save Changes</button>
    </div>
  );
}

export default App;
