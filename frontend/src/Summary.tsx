const Summary = () => {
  return (
    <div className="flex flex-col h-full items-center space-y-8">
      <video className="h-full w-full rounded-lg" controls>
        <source
          src="https://docs.material-tailwind.com/demo.mp4"
          type="video/mp4"
        />
        Your browser does not support the video tag.
      </video>

      <p className="text-2xl">This is the summary of the video lol</p>
    </div>
  );
};

export default Summary;
