# LRU algorithm added
def fifo(pages: list[int], num_frames: int) -> dict:
    frames       = []          
    frame_states = []          
    faults       = []

    for page in pages:
        if page in frames:
            faults.append(False)
        else:
            faults.append(True)
            if len(frames) < num_frames:
                frames.append(page)
            else:
                frames.pop(0)         
                frames.append(page)

        frame_states.append(list(frames))

    return {"frame_states": frame_states, "faults": faults}


def lru(pages: list[int], num_frames: int) -> dict:
    frames       = []
    frame_states = []
    faults       = []

    for i, page in enumerate(pages):
        if page in frames:
            
            frames.remove(page)
            frames.append(page)
            faults.append(False)
        else:
            
            faults.append(True)
            if len(frames) < num_frames:
                frames.append(page)
            else:
                frames.pop(0)          
                frames.append(page)

        frame_states.append(list(frames))

    return {"frame_states": frame_states, "faults": faults}


def optimal(pages: list[int], num_frames: int) -> dict:
    frames       = []
    frame_states = []
    faults       = []

    for i, page in enumerate(pages):
        if page in frames:
        
            faults.append(False)
        else:
            faults.append(True)
            if len(frames) < num_frames:
                frames.append(page)
            else:
                future = pages[i + 1:]
                farthest_idx   = -1
                page_to_replace = frames[0]

                for f in frames:
                    if f not in future:
                        
                        page_to_replace = f
                        break
                    else:
                        next_use = future.index(f)
                        if next_use > farthest_idx:
                            farthest_idx    = next_use
                            page_to_replace = f

                frames.remove(page_to_replace)
                frames.append(page)

        frame_states.append(list(frames))

    return {"frame_states": frame_states, "faults": faults}
