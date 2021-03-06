#!/usr/bin/env python3
from . import common, annotate, selection

StatisticsDict = annotate.StatisticsDict


def prepare_data_for_analysis(args, file_dict, log_file_dict):
    genome = annotate.gbk_to_seqrecord_list(args, args.genome)
    proteome = annotate.extract_features_from_genome(args, genome, 'CDS')

    StatisticsDict['NumberOfContigs'] = len(genome)
    StatisticsDict['ProteomeOrfs'] = len(proteome)

    if args.dnds_out:
        selection.full(args, file_dict, log_file_dict, skip=True)
        annotate.add_dnds_info_to_genome(args, genome, file_dict['dnds_out'])

    annotate.add_blasthits_to_genome(args, genome, log_file_dict['blastp_filename'], 'blastp')
    annotate.add_blasthits_to_genome(args, genome, log_file_dict['blastx_filename'], 'blastx')
    annotate.update_intergenic_locations(args, genome)
    return genome


def reannotate(args, genome, file_dict, visualize=False):
    annotate.find_pseudos_on_genome(args, genome)
    common.print_with_time("Collecting run statistics and writing output files.")
    annotate.analysis_statistics(args, genome)
    annotate.write_all_outputs(args, genome, file_dict, visualize)


def main():
    command_line_args = common.get_args('reannotate')
    logged_args = common.parse_log_args(command_line_args.logfile)
    args = common.reconcile_args(command_line_args, logged_args)

    file_dict = common.file_dict(args)
    log_file_dict = common.file_dict(args, outprefix=args.log_outprefix)

    genome = prepare_data_for_analysis(args, file_dict, log_file_dict)
    reannotate(args, genome, file_dict)


if __name__ == '__main__':
    main()
