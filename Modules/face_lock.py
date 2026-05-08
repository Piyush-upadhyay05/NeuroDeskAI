import cv2
import face_recognition
import os


FACE_FILE = "Data/faces/user.jpg"


# ===============================
# SAVE FACE LOCK
# ===============================
def enroll_face():

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        cv2.imshow(
            "Press S to Save Face",
            frame
        )

        key = cv2.waitKey(1)

        if key == ord("s"):

            cv2.imwrite(
                FACE_FILE,
                frame
            )

            break

        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# ===============================
# VERIFY FACE
# ===============================
def verify_face():

    if not os.path.exists(FACE_FILE):
        return False

    known_image = face_recognition.load_image_file(
        FACE_FILE
    )

    known_encoding = face_recognition.face_encodings(
        known_image
    )[0]

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        rgb = frame[:, :, ::-1]

        locations = face_recognition.face_locations(rgb)

        encodings = face_recognition.face_encodings(
            rgb,
            locations
        )

        for face_encoding in encodings:

            match = face_recognition.compare_faces(
                [known_encoding],
                face_encoding
            )

            if True in match:

                cap.release()
                cv2.destroyAllWindows()

                return True

        cv2.imshow(
            "Scanning Face...",
            frame
        )

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return False