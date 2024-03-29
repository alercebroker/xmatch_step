import numpy as np
import pandas as pd


def parse_output(lightcurves: pd.DataFrame, xmatches: pd.DataFrame, lc: dict):
    """Join xmatches with input lightcurves. If xmatch not exists for an object, the value is None.
    Also generate a list of dict as output.
    :param light_curves: Generic messages that contain the light curves (in dataframe)
    :param xmatches: Values of cross-matches (in dataframe)
    :return:
    """
    # Create a new dataframe that contains just two columns `aid` and `xmatches`.
    aid_in = xmatches["aid_in"]  # change to aid for multi stream purposes
    # Temporal code: the oid_in will be removed
    xmatches = xmatches.drop(
        columns=["ra_in", "dec_in", "col1", "aid_in"],
    )
    data = lightcurves.set_index("aid")
    if not aid_in.empty:
        xmatches.replace({np.nan: None}, inplace=True)
        xmatches = pd.DataFrame(
            {
                "aid_in": aid_in,  # change to aid name for multi stream
                "xmatches": xmatches.apply(
                    lambda x: None if x is None else {"allwise": x.to_dict()},
                    axis=1,
                ),
            }
        )
        # Join metadata with xmatches
        xmatches.rename(columns={"aid_in": "aid"}, inplace=True)
        data = data.join(xmatches.set_index("aid"))

    data.replace({np.nan: None}, inplace=True)
    data.reset_index(inplace=True)
    # Transform to a list of dicts
    data = data.to_dict("records")

    for obj in data:
        object_lc = lc[obj["aid"]]
        obj["detections"] = object_lc["detections"]
        obj["non_detections"] = object_lc["non_detections"]

    return data
