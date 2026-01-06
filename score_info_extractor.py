from music21 import stream, converter

class ScoreInfoExtractor:
    def __init__(self, score: stream.Score):
        self.score = score
        
    def get_key(self) -> str:
        return str(self.score.analyze('key'))
    
    def get_piece_name(self) -> str:
        try:
            title = self.score.metadata.title
            return title
        except:
            return "Unknown Title"

    def get_time_signatures(self) -> dict[str, list[str]]:
        """
        Return time signatures for each part (staff) in order of appearance,
        ignoring consecutive duplicates.
        
        Output format:
        {
            "Part 1": ["4/4", "2/4"],
            "Part 2": ["4/4", "2/4", "4/4"]
        }
        """
        result = {}
        for idx, part in enumerate(self.score.parts):
            ts_list = part.recurse().getElementsByClass('TimeSignature')
            part_name = part.partName or f"Part {idx+1}"

            ts_changes = []
            previous = None
            for ts in ts_list:
                ts_str = ts.ratioString
                if ts_str != previous:
                    ts_changes.append(ts_str)
                    previous = ts_str

            result[part_name] = ts_changes if ts_changes else ["Unknown"]
        
        return result



    def get_measures(self) -> str:
        return len(self.score.parts[0].getElementsByClass('Measure'))

    def get_composer(self, fallback: str = "Unknown Composer") -> str:
        try: 
            composer = self.score.metadata.composer
            return composer 
        except:
            return fallback