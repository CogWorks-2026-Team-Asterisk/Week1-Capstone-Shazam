from collections import Counter, defaultdict


def query_database(query_fingerprints, fingerprint_database):
    matches = []

    for fingerprint_hash, query_time in query_fingerprints:
        for song_id, database_time in fingerprint_database.get(
            fingerprint_hash, []
        ):
            matches.append(
                (song_id, query_time, database_time)
            )

    return matches


def tally_matches(matches, offset_precision=2):
    offset_counts = defaultdict(Counter)
    total_counts = Counter()

    for song_id, query_time, database_time in matches:
        offset = round(
            float(database_time) - float(query_time),
            offset_precision
        )

        offset_counts[song_id][offset] += 1
        total_counts[song_id] += 1

    results = {}

    for song_id, counts in offset_counts.items():
        best_offset, aligned_matches = counts.most_common(1)[0]

        results[song_id] = {
            "aligned_matches": aligned_matches,
            "total_matches": total_counts[song_id],
            "best_offset": best_offset
        }

    return results


def rank_songs(results):
    return sorted(
        results.items(),
        key=lambda item: (
            item[1]["aligned_matches"],
            item[1]["total_matches"]
        ),
        reverse=True
    )


def identify_song(
    query_fingerprints,
    fingerprint_database,
    song_metadata=None,
    minimum_matches=3,
    minimum_lead_ratio=1.2,
    offset_precision=2
):
    matches = query_database(
        query_fingerprints,
        fingerprint_database
    )

    results = tally_matches(
        matches,
        offset_precision
    )

    ranked = rank_songs(results)

    if not ranked:
        return None

    best_song_id, best_data = ranked[0]
    best_count = best_data["aligned_matches"]

    if len(ranked) > 1:
        second_count = ranked[1][1]["aligned_matches"]
    else:
        second_count = 0

    if best_count < minimum_matches:
        return None

    if second_count == 0:
        lead_ratio = float("inf")
    else:
        lead_ratio = best_count / second_count

    if lead_ratio < minimum_lead_ratio:
        return None

    result = {
        "song_id": best_song_id,
        "aligned_matches": best_count,
        "total_matches": best_data["total_matches"],
        "best_offset": best_data["best_offset"],
        "lead_ratio": lead_ratio
    }

    if song_metadata is not None:
        metadata = song_metadata.get(best_song_id, {})
        result["title"] = metadata.get(
            "title",
            str(best_song_id)
        )
        result["artist"] = metadata.get(
            "artist",
            "Unknown artist"
        )

    return result


def print_result(result):
    if result is None:
        print("No confident match found.")
        return

    title = result.get(
        "title",
        str(result["song_id"])
    )

    artist = result.get("artist", "")

    if artist:
        print(f"Song: {title} by {artist}")
    else:
        print(f"Song: {title}")

    print(
        f"Aligned matches: "
        f"{result['aligned_matches']}"
    )

    print(
        f"Total matches: "
        f"{result['total_matches']}"
    )

    print(
        f"Time offset: "
        f"{result['best_offset']}"
    )


if __name__ == "__main__":
    # Temporary test data
    test_database = {
        "hash_a": [
            ("song_1", 20.0),
            ("song_2", 50.0)
        ],
        "hash_b": [
            ("song_1", 21.5)
        ],
        "hash_c": [
            ("song_1", 23.0)
        ],
        "hash_d": [
            ("song_1", 25.0),
            ("song_2", 90.0)
        ],
        "hash_e": [
            ("song_1", 27.0)
        ]
    }

    test_query_fingerprints = [
        ("hash_a", 0.0),
        ("hash_b", 1.5),
        ("hash_c", 3.0),
        ("hash_d", 5.0),
        ("hash_e", 7.0)
    ]

    test_metadata = {
        "song_1": {
            "title": "Example Song",
            "artist": "Example Artist"
        },
        "song_2": {
            "title": "Second Song",
            "artist": "Second Artist"
        }
    }

    result = identify_song(
        test_query_fingerprints,
        test_database,
        song_metadata=test_metadata,
        minimum_matches=3
    )

    print_result(result)