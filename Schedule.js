// Store schedule and productive activities
let schedule = [];
const productiveActivities = [
    { name: 'Exercise', duration: 30, description: 'Stay healthy with a quick workout' },
    { name: 'Meditation', duration: 15, description: 'Clear your mind and reduce stress' },
    { name: 'Reading', duration: 30, description: 'Expand your knowledge' },
    { name: 'Learning a Language', duration: 30, description: 'Improve your language skills' },
    { name: 'Stretching', duration: 15, description: 'Improve flexibility and reduce tension' },
    { name: 'Journaling', duration: 15, description: 'Reflect on your thoughts and goals' },
    { name: 'Practice an Instrument', duration: 30, description: 'Develop your musical skills' },
    { name: 'Deep Work', duration: 45, description: 'Focus on important tasks' }
];

// DOM Elements
const scheduleForm = document.getElementById('scheduleForm');
const scheduleContainer = document.getElementById('scheduleContainer');
const suggestionsContainer = document.getElementById('suggestionsContainer');

// Event Listeners
scheduleForm.addEventListener('submit', handleScheduleSubmit);

// Handle form submission
function handleScheduleSubmit(e) {
    e.preventDefault();
    
    const activity = document.getElementById('activity').value;
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;

    // Validate times
    if (startTime >= endTime) {
        alert('End time must be after start time');
        return;
    }

    // Add to schedule
    schedule.push({ activity, startTime, endTime });
    
    // Sort schedule by start time
    schedule.sort((a, b) => a.startTime.localeCompare(b.startTime));
    
    // Update display
    displaySchedule();
    findFreeTimeAndSuggest();
    
    // Reset form
    scheduleForm.reset();
}

// Display schedule
function displaySchedule() {
    scheduleContainer.innerHTML = '';
    schedule.forEach(item => {
        const div = document.createElement('div');
        div.className = 'schedule-item';
        div.innerHTML = `
            <span class="activity">${item.activity}</span>
            <span class="time">${formatTime(item.startTime)} - ${formatTime(item.endTime)}</span>
        `;
        scheduleContainer.appendChild(div);
    });
}

// Format time for display
function formatTime(time) {
    return new Date('2000-01-01T' + time).toLocaleTimeString([], { 
        hour: 'numeric', 
        minute: '2-digit'
    });
}

// Find free time slots and suggest activities
function findFreeTimeAndSuggest() {
    suggestionsContainer.innerHTML = '';
    if (schedule.length === 0) return;

    const freeSlots = findFreeTimeSlots();
    freeSlots.forEach(slot => {
        const duration = getMinutesBetween(slot.startTime, slot.endTime);
        const suggestions = findSuitableActivities(duration);
        
        if (suggestions.length > 0) {
            const div = document.createElement('div');
            div.className = 'suggestion-item';
            div.innerHTML = `
                <p>Free time from ${formatTime(slot.startTime)} to ${formatTime(slot.endTime)} (${duration} minutes)</p>
                <p>Suggested activities:</p>
                <ul>
                    ${suggestions.map(activity => `
                        <li>${activity.name} (${activity.duration} mins) - ${activity.description}</li>
                    `).join('')}
                </ul>
            `;
            suggestionsContainer.appendChild(div);
        }
    });
}

// Find free time slots between scheduled activities
function findFreeTimeSlots() {
    const freeSlots = [];
    const dayStart = '06:00'; // Assume day starts at 6 AM
    const dayEnd = '22:00';   // Assume day ends at 10 PM

    // Add day start if needed
    if (schedule.length === 0 || schedule[0].startTime > dayStart) {
        freeSlots.push({
            startTime: dayStart,
            endTime: schedule.length === 0 ? dayEnd : schedule[0].startTime
        });
    }

    // Find gaps between activities
    for (let i = 0; i < schedule.length - 1; i++) {
        if (schedule[i].endTime < schedule[i + 1].startTime) {
            freeSlots.push({
                startTime: schedule[i].endTime,
                endTime: schedule[i + 1].startTime
            });
        }
    }

    // Add day end if needed
    if (schedule.length > 0 && schedule[schedule.length - 1].endTime < dayEnd) {
        freeSlots.push({
            startTime: schedule[schedule.length - 1].endTime,
            endTime: dayEnd
        });
    }

    return freeSlots;
}

// Calculate minutes between two times
function getMinutesBetween(startTime, endTime) {
    const start = new Date('2000-01-01T' + startTime);
    const end = new Date('2000-01-01T' + endTime);
    return Math.round((end - start) / 60000);
}

// Find activities that fit in the available time
function findSuitableActivities(duration) {
    return productiveActivities.filter(activity => activity.duration <= duration);
} 