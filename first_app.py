from ast import increment_lineno
import matplotlib
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import xarray as xr
#import cartopy.crs  as ccrs
import matplotlib.pyplot as plt

#xr.set_options(display_style="html")

#matplotlib.use("agg")

st.title("Processing, ploting and sharing")

st.write("For testing purpose, code is taken from this notebook https://xarray.pydata.org/en/stable/examples/monthly-means.html")

ds = xr.tutorial.open_dataset('rasm').load()

month_length = ds.time.dt.days_in_month

weights = month_length.groupby('time.season') / month_length.groupby('time.season').sum()

np.testing.assert_allclose(weights.groupby('time.season').sum().values, np.ones(4))

ds_weighted = (ds * weights).groupby('time.season').sum(dim='time')

ds_unweighted = ds.groupby('time.season').mean('time')

ds_diff = ds_weighted - ds_unweighted

notnull = pd.notnull(ds_unweighted['Tair'][0])

fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(14,12))

for i, season in enumerate(('DJF', 'MAM', 'JJA', 'SON')):
    ds_weighted['Tair'].sel(season=season).where(notnull).plot.pcolormesh(
        ax=axes[i, 0], vmin=-30, vmax=30, cmap='Spectral_r',
        add_colorbar=True, extend='both')

    ds_unweighted['Tair'].sel(season=season).where(notnull).plot.pcolormesh(
        ax=axes[i, 1], vmin=-30, vmax=30, cmap='Spectral_r',
        add_colorbar=True, extend='both')

    ds_diff['Tair'].sel(season=season).where(notnull).plot.pcolormesh(
        ax=axes[i, 2], vmin=-0.1, vmax=.1, cmap='RdBu_r',
        add_colorbar=True, extend='both')

    axes[i, 0].set_ylabel(season)
    axes[i, 1].set_ylabel('')
    axes[i, 2].set_ylabel('')

for ax in axes.flat:
    ax.axes.get_xaxis().set_ticklabels([])
    ax.axes.get_yaxis().set_ticklabels([])
    ax.axes.axis('tight')
    ax.set_xlabel('')

axes[0, 0].set_title('Weighted by DPM')
axes[0, 1].set_title('Equal Weighting')
axes[0, 2].set_title('Difference')

plt.tight_layout()

fig.suptitle('Seasonal Surface Air Temperature', fontsize=16, y=1.02)

st.write(fig)

