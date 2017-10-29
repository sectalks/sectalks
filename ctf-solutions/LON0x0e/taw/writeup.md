## Challenges

https://codewordsolver.com/anonymity/

## Challenge 1

Just grep for "Megan Fox"

634-90-4205,Megan Fox,"274 Pamela Island, Lake David, IA 23210",Actress,1-886-486-1186x9935,Sunburn

## Challenge 2

Simple CSV analysis

    require "csv"
    data = CSV.parse(open("chal2/chal2.csv"))[1..-1]
    p data.select{|x| "Cirrhosis"  == x[-1]}.map{|x| x[3] }.sort
    #=> ["Cytogeneticist", "Lawyer", "Lawyer", "Lawyer", "Museum education officer", "Pensions consultant", "Police officer", "Training and development officer"]

## Challenge 3

First we get Mike Pence's MD5-name:

    $ ruby -e 'print "Mike Pence"' | md5 #=> 82aa0d3ebbe825a5f00450bd45dcde69
    $ grep 82aa0d3ebbe825a5f00450bd45dcde69 < chal3/chal3.csv
    #=>  a4ebaebe1232cfb11b479e9b1ccc0809,82aa0d3ebbe825a5f00450bd45dcde69,47967b7b48fe685debfc314667f7920b,9375a3914f8fe5e586a48c73b0d8ca44,0d0bdbec42325ee713c1545a0b44575a,d7d2e15fce1d57157dcc4698ff488d84

Then I google hash d7d2e15fce1d57157dcc4698ff488d84 to get the answer.

## Challenge 4

First, finding all diseases for which there's more in second csv than in first:

```
    require "csv"
    a = CSV.parse(open("chal4/chal4.csv"))
    b = CSV.parse(open("chal4/chal4later.csv"))
    ht = Hash.new(0)
    b.map(&:last).each{|x| ht[x]+=1}
    a.map(&:last).each{|x| ht[x]-=1}
    ill = ht.select{|k,v| v != 0}.keys #=> ["Ingrown toenail", "Turner Syndrome", "Ovarian Cancer", "Stillbirth"]
    p b.select{|k| ill.include? k[-1]  }.map{|k| k[-1].tr(" ", "_") + k[2] }
```

Then it's just 9 entries so I brute forced that manually

## Challenge 5

Find Jill Anderson in the first data dumps:

    Abramson,17bbb461e7b1f87168907251562d6911,c02d703faa739c83b66a3db7bd35037d,243d91609c1d617e05cd20f60bc0e6a5,2694a0e5389925205b679dbe5eae7ccd

Her address hash is 17bbb461e7b1f87168907251562d6911, looking at second csv file:

    Cornelia Griggs,"1460 Claridge Drive, Beverly Hills, CA 90210",17bbb461e7b1f87168907251562d6911,Love Actually,9b3ab82b87c1a801d03c67a3a83d0234

So password is Claridge_Drive_90210

## Challenge 6

Find David Dreier:

    896-61-2854,David Dreier,"3 Santa Cruz Street, Laguna Beach, CA 92651",Politican,(087)621-2776x426,Toothache

Then use geolookup site like https://www.latlong.net/ to convert it to latlongs:

    33.532699,-117.769421

There are two matches for it in second csv (I expected some last digit fuzzing, it matches exactly):

    23691559e05b,33.532699,-117.769421

So everything for user id 23691559e05b:

    23691559e05b,33.532699,-117.769421
    23691559e05b,33.531554,-117.774201

And then check out that second one in google maps, finding out mainstreet-bar.com

## Challenge 7

Generate brute force list. Then brute force it!

    a = CSV.parse(open("movies_leak.csv"));
    guesses = a.select{|x| x[1]}.map{|x| x[1].scan(/\d+/).map{|n| x[3].tr(" ", "") + n }.map{|g| g  } }.flatten;
    guesses.each{|x| p x; system "mkdir -p tmp/#{x.shellescape}"; Dir.chdir("tmp/#{x}"){ system "unzip -P #{x.shellescape} ../../../chal8.zip" }}

After that

   rmdir tmp/*

And manually check the few that are not empty!
