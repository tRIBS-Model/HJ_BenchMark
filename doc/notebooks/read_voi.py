import os
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry import Point

def read_voi_file(filename, join=None, EPSG=None):
    """
    Returns GeoDataFrame containing voronoi polygons from tRIBS model domain.
    :param filename: Set to read _reach file specified from OUTFILENAME,but can be changed.
    :return: GeoDataFrame

    """

    ids = []
    polygons = []
    points = []
    line_count = 0

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            current_id = None
            current_voi_points = []
            current_node_points = []

            for line in file:

                line_count += 1

                if line.strip() != "END":
                    parts = line.strip().split(',')

                    if parts:
                        if len(parts) == 3:
                            id_, x, y = map(float, parts)
                            current_id = id_
                            current_node_points.append((x, y))
                        elif len(parts) == 2:
                            x, y = map(float, parts)
                            current_voi_points.append((x, y))

                elif line.strip() == "END":

                    if current_id is None:
                        break  ## catch end of file w/ two ends in a row

                    ids.append(current_id)
                    polygons.append(Polygon(current_voi_points))
                    points.append(Point(current_node_points))

                    current_id = None
                    current_voi_points = []
                    current_node_points = []

        if line_count <= 1:
            print(filename + "is empty.")
            return None


        # Package Voronoi
        if not ids or not polygons:
            raise ValueError("No valid data found in " + filename)

        voi_features = {'ID': ids, 'geometry': polygons}
        node_features = {'ID': ids, 'geometry': points}

        if EPSG is not None:
            voi = gpd.GeoDataFrame(voi_features, crs=self.geo["EPSG"])
            nodes = gpd.GeoDataFrame(node_features, crs=self.geo["EPSG"])
        else:
            voi = gpd.GeoDataFrame(voi_features)
            nodes = gpd.GeoDataFrame(node_features)
            print("Coordinate Reference System (CRS) was not added to the GeoDataFrame")


        if join is not None:
            voi = voi.merge(join, on="ID", how="inner")

            # Check for non-matching IDs
            non_matching_ids = join[~join["ID"].isin(voi["ID"])]

            if not non_matching_ids.empty:
                print("Warning: Some IDs from the dynamic or integrated data frame do not match with the voronoi IDs.")


        return voi, nodes

    else:
        print("Voi file not found.")
        return

def merge_parallel_voi(filenames, join=None, result_path=None, format=None, save=False):
    """
    Returns geodataframe of merged vornoi polygons from parallel tRIBS model run.

    :param join: Data frame of dynamic or integrated tRIBS model output (optional).
    :param save: Set to True to save geodataframe (optional, default True).
    :param result_path: Path to save geodateframe (optional, default OUTFILENAME).
    :param format: Driver options for writing geodateframe (optional, default = ESRI Shapefile)

    :return: GeoDataFrame
    """

    path_components = filenames.split(os.path.sep)
    # Exclude the last directory as its actually base name
    outfilename = os.path.sep.join(path_components[:-1])

    parallel_voi_files = [f for f in os.listdir(outfilename) if 'voi.' in f]  # list of _voi.d+ files

    if len(parallel_voi_files) == 0:
        print(f"Cannot find voi files at: {outfilename}. Returning None")
        return None

    voi_list = []
    processor_list = []
    # gdf = gpd.GeoDataFrame(columns=['ID', 'geometry'])

    for file in parallel_voi_files:
        voi = read_voi_file(f"{outfilename}/{file}")
        if voi is not None:
            voi_list.append(voi[0])
            processor = int(file.split("voi.")[-1])  # Extract processor number from file name
            processor_list.extend(np.ones(len(voi[0])) * int(processor))
        else:
            print(f'Voi file {file} is empty.')

    combined_gdf = gpd.pd.concat(voi_list, ignore_index=True)
    combined_gdf['processor'] = processor_list  # Add 'processor' column
    combined_gdf = combined_gdf.sort_values(by='ID')

    if join is not None:
        combined_gdf = combined_gdf.merge(join, on="ID", how="inner")

        # Check for non-matching IDs
        non_matching_ids = join[~join["ID"].isin(combined_gdf["ID"])]

        if not non_matching_ids.empty:
            print("Warning: Some IDs from the dynamic or integrated data frame do not match with the voronoi IDs.")

    if save:
        if result_path is None:
            result_path = os.path.join(outfilename, "_mergedVoi")

        if format is None:
            format = "ESRI Shapefile"

        combined_gdf.to_file(result_path, driver=format)

    return combined_gdf

def merge_parallel_spatial_files(outfilename, time, suffix="_00i", dtime=0, write=False, header=True, colnames=None,
                                 single=True):
    """
    Returns dictionary of combined spatial outputs for intervals specified by tRIBS option: "SPOPINTRVL".
    :param str outfilename: Path to directory where results are stored.
    :param int dtime : Option to specify time step at which to start merge of files.
    :param bool write: Option to write dataframes to file.
    :param bool header: Set to False if headers are not provided with spatial files.
    :param bool colnames: If header = False, column names can be provided for the dataframe--but it is expected the first column is ID.
    :param bool single: If single = True then only spatial files specified at dtime are merged.
    :return: Dictionary of pandas dataframes.
    """

    dyn_data = {}



    processes = 0
    otime = str(time).zfill(4)
    dynfile = f"{outfilename}.{otime}{suffix}.{processes}"

    if os.path.exists(dynfile):
        while os.path.exists(dynfile):
            if processes == 0:
                processes += 1
                try:
                    if header:
                        df = pd.read_csv(dynfile, header=0)
                    else:
                        df = pd.read_csv(dynfile, header=None, names=colnames)

                except pd.errors.EmptyDataError:
                    print(f'The first file is empty: {dynfile}.\n Can not merge files.')
                    break

                dynfile = f"{outfilename}.{otime}{suffix}.{processes}"

            else:
                processes += 1
                try:

                    if header:
                        df = pd.concat([df, pd.read_csv(dynfile, header=0)])
                    else:
                        df = pd.concat([df, pd.read_csv(dynfile, header=None, names=colnames)])

                except pd.errors.EmptyDataError:
                    print(f'The following file is empty: {dynfile}')
                dynfile = f"{outfilename}.{otime}{suffix}.{processes}"

        if header:
            df = df.sort_values(by='ID')

        if write:
            df.to_csv(f"{outfilename}.{otime}{suffix}", index=False)

        dyn_data[otime] = df

    elif os.path.exists(dynfile):
        print("Cannot find dynamic output file:" + dynfile)
 

    return dyn_data