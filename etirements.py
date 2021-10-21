import gtts
from playsound import playsound
from time import sleep
from pydub import AudioSegment
from pydub.playback import play

tts = gtts.gTTS('Récupération', lang='fr')
tts.save('repos.mp3')

circuitNames = [
  'étirements'
]

circuits = [
    [
      ('posture du cobra',40,0),
      ('obliques droit',40,0),
      ('obliques debout',40,0),
      ('grand fessier',40,0),
      ('petits et moyens fessiers',40,0),
      ('quadriceps',40,0),
      ('ischio-jambiers',40,0),
      ('posture du bébé',40,0),
      ('inclinaison avant',40,0),
      ('jambes croisées droite',20,0),
      ('jambes croisées gauche',20,0),
      ('torsion assise droite',20,0),
      ('tosion assise gauche',20,0)
    ]
    
]

beginningShift = 10


for indexCircuit, circuit in enumerate(circuits):
  tts = gtts.gTTS('Série %s'%circuitNames[indexCircuit],lang='fr')
  tts.save('tts/etirements/%s.mp3'%indexCircuit)
  for indexExo, exercise in enumerate(circuit):
    exoName = exercise[0]
    tts = gtts.gTTS('Prochain exercice : '+exoName, lang='fr')
    tts.save('tts/etirements/%s_%s.mp3'%(indexCircuit,indexExo))

print('Exercices announcements have been generated with success')

loop = AudioSegment.from_mp3('etirements.mp3')
bell = AudioSegment.from_mp3('countdown.mp3')
bell = bell.apply_gain(5)
repos = AudioSegment.from_mp3('repos.mp3')
repos = repos.apply_gain(10)

timePos = beginningShift
for indexCircuit, circuit in enumerate(circuits):
  circuitSpeech = AudioSegment.from_mp3('tts/etirements/%s.mp3'%indexCircuit)
  circuitSpeech = circuitSpeech.apply_gain(10)
  loop = loop.overlay(circuitSpeech, position=1000*(timePos-len(circuitSpeech)//1000-5))
  for indexExercise,exercise in enumerate(circuit):
    exoName = exercise[0]
    duration = exercise[1]
    pause = exercise[2]
    exoSpeech = AudioSegment.from_mp3('tts/etirements/%s_%s.mp3'%(indexCircuit,indexExercise))
    exoSpeech = exoSpeech.apply_gain(10)
    loop = loop.overlay(exoSpeech, position=1000*(timePos-len(exoSpeech)//1000-2))
    loop = loop.overlay(bell, position=1000*(timePos)) #debut exercice
    timePos+=duration
    if pause:
      loop = loop.overlay(bell, position=1000*(timePos)) #debut repos
      loop = loop.overlay(repos, position=1000*(timePos-len(repos)//1000))
      timePos+=pause
  timePos+=beginningShift

print('Audio file has been generated with success')
loop.export('ETIREMENTS_SP07.mp3',format='mp3')
#play(loop)
