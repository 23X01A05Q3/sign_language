/**
 * Gesture Detection Logic for Sign Language Interpreter
 * Based on MediaPipe Hands landmarks
 */

export const detectGesture = (landmarks) => {
    if (!landmarks || landmarks.length === 0) return "UNKNOWN";

    const tipIds = [4, 8, 12, 16, 20];
    const fingers = [];

    // Helper: Calculate distance between two landmarks
    const getDist = (p1, p2) => Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));

    // Thumb state
    const thumbOpen = landmarks[4].x > landmarks[3].x ? (landmarks[4].x > landmarks[0].x) : (landmarks[4].x < landmarks[3].x);
    fingers.push(thumbOpen ? 1 : 0);

    // Other 4 fingers
    for (let i = 1; i < 5; i++) {
        if (landmarks[tipIds[i]].y < landmarks[tipIds[i] - 2].y) {
            fingers.push(1);
        } else {
            fingers.push(0);
        }
    }

    const fingerCount = fingers.reduce((a, b) => a + b, 0);

    // 1. OK (👌) or 'F'
    if (getDist(landmarks[4], landmarks[8]) < 0.05 && fingers[2] === 1 && fingers[3] === 1 && fingers[4] === 1) {
        return "OK";
    }

    // 2. I LOVE YOU (🤟 - Thumb, Index, Pinky)
    if (fingers[0] === 1 && fingers[1] === 1 && fingers[2] === 0 && fingers[3] === 0 && fingers[4] === 1) {
        return "I LOVE YOU";
    }

    // 3. ROCK (🤘 - Index, Pinky)
    if (fingers[0] === 0 && fingers[1] === 1 && fingers[2] === 0 && fingers[3] === 0 && fingers[4] === 1) {
        return "ROCK";
    }

    // 4. CALL ME (🤙 - Thumb, Pinky)
    if (fingers[0] === 1 && fingers[1] === 0 && fingers[2] === 0 && fingers[3] === 0 && fingers[4] === 1) {
        return "CALL ME";
    }

    // 5. L-SHAPE (Index and Thumb)
    if (fingers[0] === 1 && fingers[1] === 1 && fingers[2] === 0 && fingers[3] === 0 && fingers[4] === 0) {
        return "L-SHAPE";
    }

    // 6. THUMBS UP
    if (fingers[0] === 1 && fingerCount === 1 && landmarks[4].y < landmarks[3].y) {
        return "THUMBS UP";
    }

    // 7. THUMBS DOWN
    if (fingers[0] === 1 && fingerCount === 1 && landmarks[4].y > landmarks[3].y) {
        return "THUMBS DOWN";
    }

    // 8. PEACE (✌️ - Index and Middle Apart)
    const distIndexMiddle = getDist(landmarks[8], landmarks[12]);
    if (fingers[1] === 1 && fingers[2] === 1 && fingerCount === 2 && distIndexMiddle > 0.1) {
        return "PEACE";
    }

    // 9. SHOOT (U-SHAPE - Index and Middle Together)
    if (fingers[1] === 1 && fingers[2] === 1 && fingerCount === 2 && distIndexMiddle <= 0.1) {
        return "U-SHAPE";
    }

    // 10. THREE (Index, Middle, Ring)
    if (fingers[1] === 1 && fingers[2] === 1 && fingers[3] === 1 && fingerCount === 3) {
        return "THREE";
    }

    // 11. W / SIX (Index, Middle, Ring Spread)
    if (fingers[1] === 1 && fingers[2] === 1 && fingers[3] === 1 && fingerCount === 3) {
        return "W-SHAPE";
    }

    // 12. FOUR
    if (fingers[1] === 1 && fingers[2] === 1 && fingers[3] === 1 && fingers[4] === 1 && fingerCount === 4) {
        return "FOUR";
    }

    // 13. HELLO (5)
    if (fingerCount === 5) {
        return "HELLO";
    }

    // 14. STOP / FIST
    if (fingerCount === 0) {
        return "STOP";
    }

    // 15. LITTLE (Pinky up)
    if (fingers[4] === 1 && fingerCount === 1) {
        return "LITTLE";
    }

    // 16. YES / POINT
    if (fingers[1] === 1 && fingerCount === 1) {
        return "YES";
    }

    return "UNKNOWN";
};
