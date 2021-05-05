import React from 'react'
import ReactDOM from 'react-dom'

import MeetingFeedback from './components/meeting-feedback'
import LearningCircleFeedbackForm from './components/learning-circle-feedback-form'

// Replace feedback form for earch meeting
const elements = document.getElementsByClassName('meeting-feedback-form');
for (let el of elements){
  ReactDOM.render(<MeetingFeedback {...el.dataset} />, el);
}

// Replace feedback form for learning circle
const element = document.getElementById('learning-circle-feedback-form');
ReactDOM.render(<LearningCircleFeedbackForm {...element.dataset} />, element);


