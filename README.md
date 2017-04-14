# sconce

Sconce is a dashboard for monitoring and comparing data in real time. It was built to be an easy way to visualize the training progress of different machine learning models.

![](https://i.imgur.com/cb5ExqZ.png)

## Usage

To start, create a sconce Job with a name and (optionally) parameters. Jobs with the same name will be displayed together, so you can see how different parameters affect results.

```python
import sconce

# Create a sconce job with a name and parameters
job = sconce.Job('my-neural-network', {
    'n_layers': 6,
    'hidden_size': 250,
    'learning_rate': 0.001
})
```

To plot data, call `job.record(x, y)`. Instead of posting every data point, Sconce will average the values and plot them every `plot_every` calls.

```python
# Record x, y values
for x in range(1000):
    y = train()
    job.record(x, y)
```

Then visit http://sconce.prontotype.us/jobs/my-neural-network to view your results in real time.

## Configuration

If you want more or less granularity, change `job.plot_every` and `job.print_every`:

```python
job.plot_every = 10
job.print_every = 100
```

## Private jobs

**TODO:** Register for an account and API key at http://sconce.prontotype.us/ to create private boards.

```python
sconce.login('spro', 'asdf1234uiop5768')
```
