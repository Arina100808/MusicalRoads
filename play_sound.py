import random


def play_audio(road, speed_increment=0.2):
    """
    Play an audio file and adjust audio playback speed using
    keyboard controls
    """
    # calculate number of key presses (ups, downs), store the sequence of changes
    n_presses = 0
    sequence = ""

    keyboard = Keyboard(keylist=['up', 'down', 'space', 'p'], timeout=120000)

    initial_speeds = [round(1.0 - speed_increment, 1), 1.0, round(1.0 + speed_increment, 1)]
    initial_speed = random.choice(initial_speeds)
    upper_bound = round(initial_speed + speed_increment * 2, 1)
    lower_bound = round(initial_speed - speed_increment * 2, 1)
    audio_speed = round(initial_speed, 1)
    finalized = False

    sampler = Sampler(pool[road + '.wav'])
    sampler.play(pitch=audio_speed)

    start_time = clock.time()

    while not finalized:
        # Check which key was pressed
        key, end_time = keyboard.get_key()

        if key is not None:
            if key == "up" and round(audio_speed, 1) != upper_bound:
                audio_speed += speed_increment
                n_presses += 1
                sequence += "up;"
            elif key == "down" and round(audio_speed, 1) != lower_bound:
                audio_speed -= speed_increment
                n_presses += 1
                sequence += "down;"
            # Play audio from the beginning (for example, if the audio ended)
            elif key == "p":
                pass
            elif key == "space":
                # Calculate response time
                time = end_time - start_time
                finalized = True

            sampler.stop()
            sampler = Sampler(pool[road + '.wav'])
            sampler.play(pitch=audio_speed)

    sampler.stop()

    return initial_speed, round(audio_speed, 1), time, n_presses, sequence[:-1]


# Get the path to an audio file using variables from the 'loop' item's matrix
row = items['loop'].live_dm[var.live_row]
road_name = str(row.road_nr) + row.location

init_speed, answer, response_time, number_presses, \
    changes_sequence = play_audio(road_name)
correct_answer = 1 if answer == 1.0 else 0

# additional metrics
total_correct = correct_answer if count_trial_sequence == 0 else total_correct + correct_answer
total_response_time = response_time if count_trial_sequence == 0 else total_response_time + response_time

change = round(answer - init_speed, 1)
error = round(abs(answer - 1.0), 1)
accuracy = round(total_correct / (count_trial_sequence + 1), 4)
average_response_time = round(total_response_time / (count_trial_sequence + 1), 4)

# Delete the variable from memory to avoid an 'ExperimentProcessDied' error
del row
