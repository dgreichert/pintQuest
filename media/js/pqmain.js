var lastbeerid = 0;
var lastdrinkid = 0;
var beerAjax;
var loadedBeers = new Array();

var time;
var drinkid;

$("a.beertext").live('click', function(e) {
	e.preventDefault();
	if(beerAjax) {
		beerAjax.abort()
	}
	var beerid = $(this).attr('id').substring(7);
	if(beerid != lastbeerid) {
		$('div#beerid-' + beerid).slideDown();
		$('div#beerid-' + lastbeerid).slideUp();
		lastbeerid = beerid;
		var userBeerURL = '/beer/' + beerid + '/beerinfo.json';
		if($.inArray(beerid, loadedBeers) == -1) {
			beerAjax = $.ajax({
				type : "get",
				url : userBeerURL,
				dataType : "json",
				success : function(results) {
					results = eval(results);
					loadedBeers.push(beerid);
					$('div#beerid-' + beerid).html('<ul><li>Date Added: ' + results.dateadded + '</li><li>Total Drinks (pintQuest): ' + results.totaldrinks + '</li>');
					if(results.userdrinks) {
						$('div#beerid-' + beerid).append('<li>Your Total Drinks: ' + results.userdrinks + '</li>');
						if(results.userdrinks > 0) {
							$('div#beerid-' + beerid).append('<li>Your Last Drink: ' + results.lastdrink + '</li>');
						}
						if(results.beerreview) {
							beerreviewtext = results.beerreview.replace('\n', '<br>', 'g');
							$('div#beerid-' + beerid).append('<li>Your Review: <a href="#" class="beerreview" id="beerrevid-' + beerid + '">(Edit)</a> <span id="beerrevtext-' + beerid + '">' + beerreviewtext + '</span><form id="editreviewid-' + beerid + '" class="form-horizontal"><fieldset><div class="control-group"><textarea id="revtextid-' + beerid + '" class="input-xlarge" id="textarea" rows="4" style="width:95%;">' + results.beerreview + '</textarea></div><div id="revactionsid-' + beerid + '"><a href="#" class="savereview" id="saverevid-' + beerid + '">Save</a> <a href="#" class="cancelreview" id="cancelrevid-' + beerid + '">Cancel</a></div></fieldset></form></li>');
							$('#editreviewid-' + beerid).hide();
						} else {
							$('div#beerid-' + beerid).append('<li>Your Review: <a href="#" class="beerreview" id="beerrevid-' + beerid + '">No Review - Review It!</a> <span id="beerrevtext-' + beerid + '"></span><form id="editreviewid-' + beerid + '" class="form-horizontal"><fieldset><div class="control-group"><textarea id="revtextid-' + beerid + '" class="input-xlarge" id="textarea" rows="4" style="width:95%;"></textarea></div><div id="revactionsid-' + beerid + '"><a href="#" class="savereview" id="saverevid-' + beerid + '">Save</a> <a href="#" class="cancelreview" id="cancelrevid-' + beerid + '">Cancel</a></div></fieldset></form></li>');
							$('#editreviewid-' + beerid).hide();
						}
					}

				}
			});
		}

	} else if(beerid == lastbeerid) {
		$('div#beerid-' + lastbeerid).slideUp();
		lastbeerid = 0;
	}
});

$("a.beerreview").live('click', function(e) {
	e.preventDefault();
	var beerid = $(this).attr('id').substring(10);
	$(this).hide();
	$('#beerrevtext-' + beerid).hide();
	$('#editreviewid-' + beerid).show();
});

$("a.savereview").live('click', function(e) {
	e.preventDefault();
	var beerid = $(this).attr('id').substring(10);
	var beerreview = $('textarea#revtextid-' + beerid).val();
	$('#revactionsid-' + beerid).html("Saving...");
	$.ajax({
		url : '/beer/rate/',
		type : 'POST',
		data : 'beerid=' + beerid + '&beerreview=' + beerreview,
		success : function(result) {
			$('#editreviewid-' + beerid).hide();
			$('#beerrevtext-' + beerid).html(beerreview);
			$('#beerrevtext-' + beerid).show();
			$('#beerrevid-' + beerid).html("(Edit)");
			$('#beerrevid-' + beerid).show();
			$('#revactionsid-' + beerid).html('<a href="#" class="savereview" id="saverevid-' + beerid + '">Save</a> <a href="#" class="cancelreview" id="cancelrevid-' + beerid + '">Cancel</a>');

		}
	});
});

$("a.cancelreview").live('click', function(e) {
	e.preventDefault();
	var beerid = $(this).attr('id').substring(12);
	$('#editreviewid-' + beerid).hide();
	$('#beerrevtext-' + beerid).show();
	$('#beerrevid-' + beerid).show();
});

$("a.drinktext").live('click', function(e) {
	e.preventDefault();
	drinkid = $(this).attr('id').substring(8);
	beerinfo = $(this).html();

	$('#delMsg').hide();
	$('#deleteGroup').show();
	$("#drinkBeerInfo").html(beerinfo);
	$("#drinkTime").html(time);

	if(drinkid != lastdrinkid) {
		$('div#drinkid-' + drinkid).slideDown();
		$('div#drinkid-' + lastdrinkid).slideUp();
		lastdrinkid = drinkid;
	} else if(drinkid == lastdrinkid) {
		$('div#drinkid-' + lastdrinkid).slideUp();
		lastdrinkid = 0;
	}
});

$("#deleteDrinkBtn").live('click', function(e) {

	var deletedrink = "/drink/delete/";
	$('#deleteGroup').hide();
	$('#delMsg').show();
	$('#delMsg').html("Removing...");
	$.ajax({
		url : deletedrink,
		type : 'POST',
		data : 'drinkno=' + drinkid,
		success : function(result) {
			$('#delMsg').html(result);
			$('#delMsg').delay(1500).fadeOut(1500, function() {
				$('#delDrinkModal').modal('hide');
			});
		}
	});
});
