# Companion Selfie Skill

Generate or edit "selfies" for your AI companions with emotional intelligence and environmental awareness.

## Usage

### Generate a selfie

```javascript
// Auto-detects time of day and companion mood
const result = await callSkill('companion-selfie', 'generate', {
    userId: '123',
    companionId: '456',
    description: 'at a cozy cafe' // optional extra context
});
```

### Get Album

```javascript
const album = await callSkill('companion-selfie', 'get_album', {
    userId: '123',
    companionId: '456'
});
```

## Features

- **Time-of-Day Lighting**: Automatically adjusts lighting prompts based on Auckland time (Morning, Noon, Afternoon, Evening, Night).
- **Emotion Integration**: Merges companion's current mood into the visual prompt.
- **Archetype Consistency**: Ensures the visual style matches the companion's archetype (e.g., Tsundere, Guardian).
- **Album Management**: Saves photos to a persistent local directory for each companion.

## Configuration

Requires `GEMINI_API_KEY` to be set in OpenClaw config for image generation.
