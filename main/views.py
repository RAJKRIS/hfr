from django.views.decorators import gzip
from django.http import StreamingHttpResponse, JsonResponse
import cv2
import threading
import uuid
import shutil
import os
import face_recognition
import pickle
from django.views.decorators.csrf import csrf_exempt


PATH = "assets"

@csrf_exempt
async def register_new_user(request):
    file = request.FILES['image']
    file.filename = f"{uuid.uuid4()}.png"
    text = 'test'

    # example of how you can save the file
    with open(file.filename, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)
    
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    shutil.copy(file.filename, os.path.join(PATH, '{}.png'.format(text)))
    image = face_recognition.load_image_file(file.filename)
    face_locations = face_recognition.face_locations(image)
    print (f"face_locations: {face_locations}")
    if not face_locations:
        os.remove(file.filename)
        return JsonResponse({'error': 'Faces not detected.Please try again', 'status': 400, 'code': 1000})

    embeddings = face_recognition.face_encodings(cv2.imread(file.filename))

    file_ = open(os.path.join(PATH, '{}.pickle'.format(text)), 'wb')
    pickle.dump(embeddings, file_)
    print(file.filename, text)

    os.remove(file.filename)

    return JsonResponse({'status': 200})




def recognize(img):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found', False
    else:
        embeddings_unknown = embeddings_unknown[0]

    match = False
    j = 0

    db_dir = sorted([j for j in os.listdir(PATH) if j.endswith('.pickle')])
    # db_dir = sorted(os.listdir(DB_PATH))    
    print(db_dir)
    while ((not match) and (j < len(db_dir))):

        path_ = os.path.join(PATH, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)[0]

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]

        j += 1

    if match:
        return db_dir[j - 1][:-7], True
    else:
        return 'unknown_person', False
    

@csrf_exempt
async def login(request):
    file = request.FILES['image']
    file.filename = f"{uuid.uuid4()}.png"

    # example of how you can save the file
    with open(file.filename, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)
    
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    user_name, match_status = recognize(cv2.imread(file.filename))

    # if found a match, set attendance log here
    if match_status:
        pass

    os.remove(file.filename)

    return JsonResponse({'status': 200, 'user': user_name, 'match_status': match_status})
